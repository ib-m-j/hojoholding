import argparse
import shutil
import os.path
import ftplib
import io
import sys
import re

#filename, search string, replace string)
toDeploy = [
    ("html/allmexico.html",'file:./', 'http://getgoodtaste.com/Maps/'),
    ("html/central.html",None,None),
    ("html/northeast.html",None,None),
    ("html/northwest.html",None,None),
    ("html/east.html",None,None),
    ("html/south.html",None,None),
    ("../html/mexicohigh.html",None,None),
    ("../html/zoom.html",None,None)
    ]

target = "../../Google\ Drive/hojoholding/html"




def doDeploy():
    for f in toDeploy:
        print("Moving " + f)
        shutil.copyfile(f, os.path.join("c:\\","Users","Ib", "Google Drive", "hojoholding", "html", os.path.basename(f)))

def ftpDeploy():
    ftpconn = ftplib.FTP(host="veramexicana.com", user="veramexi", passwd="PelleSoren1988")
    #print(ftpconn.login())
    print(ftpconn.cwd("public_html/getgoodtaste.com/Maps"))
    print(ftpconn.retrlines('LIST'))
    for f in toDeploy:
        data = open(f, 'rb')
        ftpconn.storlines('STOR {}'.format(os.path.basename(f)), data)
        print('uploaded', os.path.basename(f))
        data.close()

    print(ftpconn.quit())
    print("ended")


def testFtpString():
        #below needed for ftp use string as file
    dataFile = open(toDeploy[0], 'r')
    openeds =io.StringIO(dataFile.read())
    dataFile.close()
    
    while True:
        l=openeds.readline()
        if not l:
            break
        print(l,)
    openeds.close()

def ftpDeployWithReplacement():
    ftpconn = ftplib.FTP(host="veramexicana.com", user="veramexi", passwd="PelleSoren1988")
    print(ftpconn.cwd("public_html/getgoodtaste.com/Maps"))
    print(ftpconn.retrlines('LIST'))
    try:
        for (fName, search, replace) in toDeploy:
            if search:
                print("Replacing: File {}, Search {}, Replace {}".format(fName, search, replace))
                dataFile = open(fName, 'r')
                dataText = dataFile.read()
                dataFile.close()
                res = re.sub(search, replace, dataText)
                dataTextFilelike = io.BytesIO(res.encode('utf-8'))
                ftpconn.storlines('STOR {}'.format(os.path.basename(fName)), dataTextFilelike)
                print('uploaded', os.path.basename(fName))
            else:
                data = open(fName, 'rb')
                ftpconn.storlines('STOR {}'.format(os.path.basename(fName)), data)
                print('uploaded', os.path.basename(fName))
                data.close()
                
    except:
        print(sys.exc_info())

    print(ftpconn.quit())
    print("ended")


    
if __name__ == '__main__':
    #ftpDeploy()
    #testFtpString()
    ftpDeployWithReplacement()
