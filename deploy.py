import shutil
import os.path

toDeploy = [
    "html/allmexico.html",
    "html/central.html",
    "html/northeast.html",
    "html/northwest.html",
    "html/east.html",
    "html/south.html",
    "mexicohigh.html"
    ]

target = "../../Google\ Drive/hojoholding/html"




for f in toDeploy:
    print("Moving " + f)
    shutil.copyfile(f, os.path.join("c:\\","Users","Ib", "Google Drive", "hojoholding", "html", os.path.basename(f)))

