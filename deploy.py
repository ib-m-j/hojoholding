import argparse
import shutil
import os.path
import ftplib
import io

toDeploy = [
    "html/allmexico.html",
    "html/central.html",
    "html/northeast.html",
    "html/northwest.html",
    "html/east.html",
    "html/south.html",
    "../html/mexicohigh.html",
    "../html/zoom.html"
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

        
if __name__ == '__main__':
    #below needed for ftp use string as file
    openeds =io.StringIO("aslkfj\nasifu\n")
    
    while True:
        l=openeds.readline()
        if not l:
            break
        print(l)
    openeds.close()
