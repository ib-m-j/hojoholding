import xml.dom.minidom as dom
import re
import sys


typeMatch = '[MmLlHhVvZz]'
numberMatch = '(-?[0-9]+(\.[0-9]+)?)'
pointMatch ='('+numberMatch+','+numberMatch+')'
typeMatcher = re.compile(typeMatch)
numberMatcher = re.compile(numberMatch)
pointMatcher = re.compile(pointMatch)


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

    def getTrueLocation(self):
        return self.location


    def __str__(self):
        return '({0:.2f}, {1:.2f}) '.format(self.location[0], self.location[1])
    
class SvgPath:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.elements = []
        self.relativeLocation = False
        self.lastLocation =()
        
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
        for x in self.elements:
            part = '\nElement number: {}\n'.format(counter)
            for p in x:
                part = part + p.__str__()
            res = res + part
            counter += 1
        return res
            

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


    
#globalPaths = []

#def resolvePath(p, current):
#    if len(p) == 0:
#        print("returning")
#        #print(current)
#        globalPaths.append(current)
#        #print(globalPaths)
#        return
#    
#    next = typeMatcher.match(p)
#    if not(next):
#        raise(Exception('expected a type' + p[0:10]))
#
#    #print(next.group(0))
#    pointType = next.group(0)
#    if pointType in 'MmLl':
#        next = pointMatcher.match(p[1:])
#        try:
#            #print(next.groups())
#            if pointType in 'Mm':
#                if current:
#                    globalPaths.append(current[:])
#                #print('setting current')
#                #print(globalPaths)
#                current = []
#
#            x = float(next.group(2))
#            y = float(next.group(4))
#            current.append((x,y))
#            #if pointType == 'M' and current:
#            #    print(all)
#            #    sys.exit()
#            #print(x,y)
#            nextStart = next.end() + 1
#        except:
#            raise Exception('failed l ' + p[:10])
#            
#    elif pointType in 'VvHh':
#        next = numberMatcher.match(p[1:])
#        x = float(next.group(1))
#        if next.group(0) in 'Vv':
#            current.append((current[-1][0], current[-1][1]+x))
#        else:
#            current.append((current[-1][0] + x, current[-1][1]))
#            
#        #print(x)
#        nextStart = next.end() + 1
#
#    elif pointType in 'Zz':
#        current.append(current[0])
#        nextStart = next.end()
#        
#    resolvePath(p[nextStart:], current)
#

#def resolvePath(p):
#    if len(p) == 0:
#        return
#    next = nextMatch.match(p)
#    if next:
#        print(next.groups())
#        print(next.end())
#        resolvePath(p[next.end():])
#    else:
#        print('exiting',p[0:10])
#        #next = nextMatch.match(p[next.end():])
#        sys.exit()
#



domTree = dom.parse("mexicoHigh.svg")
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


for k,v in allres.items():
    print(v)
print("finished")         


      
