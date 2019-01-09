import sys
import parsesvg
import string

def dumpData(allres):        
    f1 = open("dumpoverview.txt",'w')
    f2 = open('dumpcleaned.txt','w')
    for k,v in allres.items():
        f1.write(v.overview('cleaned'))
        v.setLevel('cleaned')
        f2.write(v.__str__())
        #print(v.overview('rawdata'))
        #print(v.overview('cleaned'))
    
    f1.close()
    f2.close()


def compareIter(allres):
    active = allres['MX-AGU']
    active.setLevel('rawdata')
    counter = 0
    for x in active:
        counter +=1
    print('rawdata', counter)

    active.setLevel('cleaned')
    counter = 0
    for x in active:
        counter +=1
    print('rawdata', counter)
    


def setBorders(allres, dev = False):    
    keys = list(allres.keys())
    #f1 = open('borderoverview.txt','w')
    #f2 = open('borderraw.txt','w')
    for (n,k1) in enumerate(keys):
        if dev and n>2:
            break
        print(allres[k1].id)
        for k2 in keys[n+1:]:
            #print(k1, k2)
            for e1 in allres[k1]:
                for e2 in allres[k2]:
                    if e1 == e2:
                        #print('found one', e1,e2)
                        if not (allres[k1].id in e2.borders):
                                e2.borders.append(allres[k1].id)
                        #e2.borders.append(allres[k1].id)
                        if not (allres[k2].id in e1.borders):
                                e1.borders.append(allres[k2].id)

        #f1.write(allres[k1].borderOverview('cleaned'))
        #f2.write(allres[k1].borderRaw('cleaned'))

    #f1.close()
    #f2.close()

def dumpSvgData(allres, classMap, level, number, filename):
    f = open(filename, 'w')
    res = ''
    counter = 0
    for v in allres.values():
        res = res + v.dumpSvg(level, classMap )
    f.write(res)
    f.close()

    #below writes ids in not quite useful location
    #f=open('idtexts.txt', 'w')
    #for path in allres.values():
    #    x = path.elements[0][0].getTrueLocation()[0]
    #    y =  path.elements[0][0].getTrueLocation()[1]
    #    f.write('<text class="idname" x={} y={}>{}</text>\n' .
    #            format(x,y,path.id))
    #
    #f.close()
    


    
def svgData(allres, classMap, level):
    res = ''
    for v in allres.values():
        res = res + v.dumpSvg(level, classMap )
    return res

def reducedata():
    #too reduced does not work
    allres = parsesvg.readSvgFile("mexicoHigh.svg")
    setBorders(allres)

    counter = 0
    res = ''
    for path in allres.values():
        path.reduce(1, 'cleaned', 'reduced4')
        #print(path.borderOverview('reduced4'))
        counter += 1
        res = res + path.dumpSvg('reduced4')
        if counter == 100:
            break
 
    f = open('svgdata.txt', 'w')
    f.write(res)
    f.close()

def removeIslands(allres):
    counter = 0
    res = ''
    for path in allres.values():
        path.removeIslands('cleaned', 10, 'islands10')
        counter += 1
        res = res + path.dumpSvg('islands10', regionDef)
 
    f = open('svgislands.txt', 'w')
    f.write(res)
    f.close()


def makeRegions(allres, level, regionDefs):
    regionNames = list(set(regionDefs.values()))
    allRegionCoordinates = {}
    allRegionBoxes = {}
    for name in regionNames:
        allRegionCoordinates[name] = ''
        allRegionBoxes[name] = parsesvg.BoundingBox()

    for path in allres.values():
        myRegion = regionDefs[path.id]

        pathDesc = '<path id =\"{}\" title =\"{}\" \
        onclick=\"showId()\" class =\"{}\" d=\"{}\"/>\n'.format(
            path.id, path.name,  regionDefs[path.id],
            path.dumpSvg(level, regionDefs))

        allRegionCoordinates[myRegion] += pathDesc
        allRegionBoxes[myRegion].includeValue(path.findBound(level))
            
    template = open('regiontemplate.html', 'r')
    templateText = template.read()
    template.close()


    for region in regionNames:
        resName = 'html/' + region + '.html'
        f = open(resName, 'w')
        newTemplate = string.Template(templateText)
        sub = dict(paths=allRegionCoordinates[region],
                   viewBox=allRegionBoxes[region].topLeftSizeString(),
                   title='Mexico - {}'.format(region)
        )
        f.write(newTemplate.substitute(sub))
        f.close()
        print("Wrote ", resName)
        print("Bounds: " + allRegionBoxes[region].__str__())
        print("also: " + allRegionBoxes[region].topLeftSizeString() + '\n')
    

def makeMexico(allres, level, regionDefs):
    bB = parsesvg.BoundingBox()
    allCoordinates = ''
    for path in allres.values():
        pathDesc = '<path id =\"{}\" title =\"{}\" \
        onclick=\"gotoRegion(\'file:./{}.html\')\" class =\"{}\" d=\"{}\"/>\n'.format(
            path.id, path.name,  regionDefs[path.id], regionDefs[path.id],
            path.dumpSvg(level, regionDefs))

        allCoordinates  += pathDesc
        bB.includeValue(path.findBound( level))

    file = open("mexicotemplate.html","r")
    template = string.Template(file.read())
    file.close()

    sub = dict(paths=allCoordinates, viewBox=bB.topLeftSizeString())
    
    resName = 'html/allmexico.html'
    f = open(resName, 'w')
    f.write(template.substitute(sub))
    f.close()
    print("Wrote " + resName)
    print("Bounds: " + bB.__str__())
    print("also: " + bB.topLeftSizeString() + '\n')


regionDef =\
{"MX-AGU":"central",
 "MX-BCN":"northwest",
 "MX-BCS":"northwest",
 "MX-CAM":"east",
 "MX-CHP":"east",
 "MX-CHH":"northeast",
 "MX-COA":"northeast",
 "MX-COL":"central",
 "MX-OCL":"central",
 "MX-DIF":"central",
 "MX-DUR":"northwest",
 "MX-GUA":"central",
 "MX-GRO":"south",
 "MX-HID":"central",
 "MX-JAL":"central",
 "MX-MEX":"central",
 "MX-MIC":"central",
 "MX-MOR":"central",
 "MX-NAY":"central",
 "MX-NEL":"northeast",
 "MX-NLE":"central",
 "MX-OAX":"south",
 "MX-PUE":"central",
 "MX-QUE":"central",
 "MX-ROO":"east",
 "MX-SLP":"northeast",
 "MX-SIN":"northwest",
 "MX-SON":"northwest",
 "MX-TAB":"east",
 "MX-TAM":"northeast",
 "MX-TLA":"central",
 "MX-VER":"central",
 "MX-YUC":"east",
 "MX-ZAC":"northwest"
}

def svgDescription(allres, level):
    res = ''
    minX = 10000
    maxX = 0
    minY = 10000
    maxY = 0
    for v in allres.values():
        allInfo = v.describeSvgPath(level)
        res = res + allInfo[0]
        newBounds = allInfo[1:]
        if newBounds[0] < minX:
            minX = newBounds[0]
        if newBounds[1] > maxX:
            maxX = newBounds[1]
        if newBounds[2] < minY:
            minY = newBounds[2]
        if newBounds[3] > maxY:
            maxY = newBounds[3]

    pathsDesc = open('pathsdescription.txt', 'w')
    
    print(res)
    pathsDesc.write(res)
    
    print("Bounds: ", minX, maxX, minY, maxY)
    pathsDesc.write("Bounds: " + '{} '.format(minX)
                    + '{} '.format(maxX)
                    + '{} '.format(minY)
                    + '{} '.format(maxY) )
    pathsDesc.close()


def makeHtmls():
    allres = parsesvg.readSvgFile("mexicoHigh.svg")
    #setBorders(allres, True)
    removeIslands(allres)
    makeMexico(allres, 'islands10', regionDef)
    makeRegions(allres, 'islands10', regionDef)
    
    
if __name__ == '__main__':
    makeHtmls()
    #allres = parsesvg.readSvgFile("mexicoHigh.svg")
    #removeIslands(allres)
    #counter = 0
    #for res in allres.values():
    #    bb = res.findBound('islands10')
    #
    #    print(res.describeSvgPath('islands10'))
    #    counter = counter + 1
    #    if counter == 1:
    #        break
        
    #setBorders(allres, True)
    #svgDescription(allres, 'islands10')

    #print(template)
    #htmlFile= open("cleanedregionislands.html","w")
    #htmlFile.write(template.replace('@',
    #    svgData(allres, regionDef, 'islands10')))
    #htmlFile.close()

    #path = allres['MX-BCN']
    #
    #print(path.borderRaw('cleaned'))
    #path.reduce(4, 'cleaned', 'reduced4')
    #print(path.borderRaw('reduced4'))
    #print(path.borderOverview('reduced4'))
