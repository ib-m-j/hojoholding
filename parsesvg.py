import sys
import xml.dom.minidom as dom
import re



class svgPathPoint:
    def __init__(self, relativeLocation, new, last):
        newX = new[0]
        newY = new[1]
        self.isRelative = relativeLocation
        if relativeLocation:
            lastX = last.getTrueLocation()[0]
            lastY = last.getTrueLocation()[1]
            self.location = (newX + lastX, newY + lastY)
        else:
            self.location = (newX, newY)

        self.borders = []
            
    def getTrueLocation(self):
        return self.location

    def __eq__(self, a):
        return self.getTrueLocation() == a.getTrueLocation()

    def __str__(self):
        return '({0:.2f}, {1:.2f}) '.format(self.location[0], self.location[1])


#this function works on list of pathpoints - an intermediary between
#svgpathpont and svgpath
def findBound(element):
    minX = 100000
    minY = 100000
    maxX = 0
    maxY = 0

    for p in element:
        (x,y) = p.getTrueLocation()
        if x < minX:
            minX = x
        elif x > maxX:
            maxX = x
        if y < minY:
            minY = y
        elif y > maxY:
            maxY = y

    return(minX, maxX, minY, maxY)


    
class SvgPath:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.paths = {}
        self.elements = []
        self.paths['rawdata'] = self.elements
        self.relativeLocation = False
        self.lastLocation =()
        self.currentLevel = 'rawdata'
        
#    def getTrueLocation(self, (newX, newY)):
#        try:
#            if self.relativeLocation:
#                (lastX, lastY) = self.openElement[-1]
#                return (newX + lastX, newY + lastY)
#        
#            return (newX, newY)
#        except:
#            raise Exception('gor relativelocation with no openelemen')
#

    def addPoint(self, type, location):
        if type in 'lmvh':
            if type == 'h':
                location = (location[0], 0)
            elif type == 'v':
                location = (0, location[0])
                
            nextPoint = svgPathPoint(True, location, self.lastLocation)
            
        elif type in 'LVMH':
            if type == 'H':
                location = (location[0], self.lastLocation.getTrueLocation()[1])
            elif type == 'V':
                location = (self.lastLocation.getTrueLocation()[1], location[0])
                
            nextPoint = svgPathPoint(False, location, ())

        elif type in 'zZ':
            nextPoint = svgPathPoint(
                False, self.openElement[0].getTrueLocation(), None)
        else:
            print('Unknown type in addPoint: ', type)
            sys.exit(1)
                                     
        if type in 'mM':
            #if hasattr(self, 'openElement'):
            #    self.elements.append(self.openElement)
            #    
            self.openElement = [nextPoint]
            self.elements.append(self.openElement)

        else:
            self.openElement.append(nextPoint)

        self.lastLocation = nextPoint
            
    def __str__(self):
        res = '\nId: {}, Name = {}\n'.format(self.id, self.name)
        counter = 0
        for x in self.paths[self.currentLevel]:
            part = '\nElement number: {}\n'.format(counter)
            for p in x:
                part = part + p.__str__()
            res = res + part
            counter += 1
        return res

    def scan(self, pathLevel):
        path = self.paths[pathLevel]
        for sP in path:
            for p in sP:
                yield(p)
    
    def overview(self, pathLevel):
        res = '\nId: {}, Name = {}\n'.format(self.id, self.name)
        counter = 0
        for x in self.paths[pathLevel]:
            part = 'Element number: {}, size {}\n'.format(counter, len(x))
            res = res + part
            counter += 1
        return res

    def borderOverview(self, pathLevel):
        res = '\nId: {}, Name = {}\n'.format(self.id, self.name)
        elementCounter = 0
        for sP in self.paths[pathLevel]:
            #print(self.id)
            #print(x.borders)
            lastBorders = None
            res = res + 'Element {}\n'.format(elementCounter)
            counter = 0
            for (n,point) in enumerate(sP):
                currentBorders = self.id + ',' + str.join(',',point.borders)
                if (currentBorders) != (lastBorders or n == len(sP) - 1):
                    res = res + '{} length: {} point ({:.2f}, {:.2f})\n'.format(
                        currentBorders, counter, point.getTrueLocation()[0],
                        point.getTrueLocation()[1])
                    lastBorders = currentBorders
                    counter = 0
                else:
                    counter += 1
            elementCounter = elementCounter +1
            res = res + '{} length: {}\n'.format(lastBorders, counter)
                
        return res

    def borderRaw(self, pathLevel):
        res = '\nId: {}, Name = {}'.format(self.id, self.name)
        counter = 0
        for sP in self.paths[pathLevel]:
            res = res + '\nElement {} length {}'.format(counter, len(sP))
            for point in sP:
                res = res + '\n{}  {}'.format(point, point.borders)
            counter += 1
            
        return res
    
    def basicClean(self):
        cleaned = []
        self.paths['cleaned'] = cleaned
        for subPath in self.paths['rawdata']:
            newSub = []
            for element in subPath:
                if len(newSub) == 0 or element != newSub[-1]:
                    newSub.append(element)
                else:
                    pass
            cleaned.append(newSub)

        self.setLevel('cleaned')
        
    def setLevel(self, x):
        self.currentLevel = x
            
    def __iter__(self):
        for sP in self.paths[self.currentLevel]:
            for e in sP:
                yield(e)
        

    def reduce(self, smallest, level, resLevel):

        def reduceBy(smallest, breaks):
            newBreaks = [0]
            for b in breaks:
                lastBreak = newBreaks[-1]
                nextGap = b - lastBreak
                newSpace = nextGap//smallest
                if newSpace == 0:
                    newSpace = 1
                for x in range(1, (nextGap // newSpace)):
                    newBreaks.append(lastBreak + x*newSpace)
                        
                if lastBreak != b:
                    newBreaks.append(b)
            return(newBreaks)


        path = []
        for sP in self.paths[level]:
            breaks = []
            lastBorders = None
            for (n,e) in enumerate(sP):
                if (e.borders == lastBorders) and (n != (len(sP) - 1)):
                    pass
                else:
                   breaks.append(n)
                   lastBorders = e.borders
                   if n == len(sP) - 1 and breaks[-1] != len(sP) - 1:
                       breaks.append(len(sP) - 1)
    
            newBreaks = reduceBy(smallest, breaks)
            #print(breaks, newBreaks)      
            newSubPath = []
            for b in newBreaks:
                newSubPath.append(sP[b])
            path.append(newSubPath)

        self.paths[resLevel] = path

    def removeIslands(self, level, size, resLevel):
        path = []
        for sP in self.paths[level]:
            (xMin, xMax, yMin, yMax) =  findBound(sP)
            if ((xMax - xMin) > size or (yMax - yMin) > size):
                path.append(sP)

        self.paths[resLevel] = path

    def dumpSvg(self, level, classMap):
        #improve by using function makeLocationData below
        path = self.paths[level]
        locationData = self.makeLocationData(level)
# for sP in path:
#     locationData = locationData + '{}{:.2f},{:.2f}'.format(
#         'M', sP[0].getTrueLocation()[0], sP[0].getTrueLocation()[1])
#     for point in sP[1:-1]:
#         locationData = locationData + '{}{:.2f},{:.2f}'.format(
#         'L', point.getTrueLocation()[0], point.getTrueLocation()[1])
#     locationData = locationData + '{}'.format('z')
#
        res = '<path id =\"{}\" title =\"{}\" \
        onclick="showId()" class =\"{}\" d=\"{}\"/>\n'.format(
            self.id, self.name, classMap[self.id], locationData)
        return res

    def makeLocationData(self, level):
        path = self.paths[level]
        locationData = ''
        for sP in path:
            locationData = locationData + '{}{:.2f},{:.2f}'.format(
                'M', sP[0].getTrueLocation()[0], sP[0].getTrueLocation()[1])
            for point in sP[1:-1]:
                locationData = locationData + '{}{:.2f},{:.2f}'.format(
                'L', point.getTrueLocation()[0], point.getTrueLocation()[1])
            locationData = locationData + '{}'.format('z')

        return locationData

    
    def describeSvgPath(self, level):
        path = self.paths[level]

        res = 'Path id: {} title: {}\n'.format(
            self.id, self.name)

        glminX = 100000
        glminY = 100000
        glmaxX = 0
        glmaxY = 0
        
    
        counter = 0
        for sP in path:
            (minX, maxX, minY, maxY) = findBound(sP)
            res = res + 'Element: {} Bounds: {} {} {} {}\n'.format(
                counter, minX, maxX, minY, maxY)
            counter += 1
            if minX < glminX:
                glminX = minX
            if maxX > glmaxX:
                glmaxX = maxX
            if minY < glminY:
                glminY = minY
            if maxY > glmaxY:
                glmaxY = maxY

        return (res + '\n', glminX, glmaxX, glminY, glmaxY)
                

#----------------------------------------------------------------------
                
typeMatch = '[MmLlHhVvZz]'
numberMatch = '(-?[0-9]+(\.[0-9]+)?)'
pointMatch ='('+numberMatch+','+numberMatch+')'
typeMatcher = re.compile(typeMatch)
numberMatcher = re.compile(numberMatch)
pointMatcher = re.compile(pointMatch)


def resolvePath(p, svgPath):
    if len(p) == 0:
        #print("returning")
        return
    
    next = typeMatcher.match(p)
    if not(next):
        raise(Exception('expected a type' + p[0:10]))

    #print(next.group(0))
    #print(next.groups())
    pointType = next.group(0)
    if pointType in 'MmLl':
        #print(p[1:10])
        next = pointMatcher.match(p[1:])
        #print(next.groups())
        x = float(next.group(2))
        y = float(next.group(4))
        loc = (x,y)
        nextStart = next.end() + 1
            
    elif pointType in 'VvHh':
        next = numberMatcher.match(p[1:])
        x = float(next.group(1))
        loc = (x,)
        nextStart = next.end() + 1

    elif pointType in 'Zz':
        loc = ()
        nextStart = next.end()

    #print(pointType, loc)
    svgPath.addPoint(pointType, loc)
    
    resolvePath(p[nextStart:], svgPath)


def readSvgFile(fileName):
    
    domTree = dom.parse(fileName)
    collection = domTree.documentElement

    paths = collection.getElementsByTagName('path')


    borders = {}


    allres = {}
    for path in paths:
        id = path.getAttribute('id')
        name = path.getAttribute('title')
        nextPath = SvgPath(id, name)
        data = path.getAttribute('d')
        #print(data[:20])
        resolvePath(path.getAttribute('d'), nextPath)
        allres[id] = nextPath
        nextPath.basicClean()

                
    return allres



