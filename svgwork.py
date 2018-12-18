import parsesvg


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
    

def setBorders(allres):    
    keys = list(allres.keys())
    #f1 = open('borderoverview.txt','w')
    #f2 = open('borderraw.txt','w')
    for (n,k1) in enumerate(keys):
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



        
if __name__ == '__main__':
    allres = parsesvg.readSvgFile("mexicoHigh.svg")
    setBorders(allres)

    counter = 0
    for path in allres.values():
        path.reduce(4, 'cleaned', 'reduced4')
        print(path.borderOverview('reduced4'))
        counter += 1
        if counter == 100:
            break
        

    #path = allres['MX-BCN']
    #
    #print(path.borderRaw('cleaned'))
    #path.reduce(4, 'cleaned', 'reduced4')
    #print(path.borderRaw('reduced4'))
    #print(path.borderOverview('reduced4'))
