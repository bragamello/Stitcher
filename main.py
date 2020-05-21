##controls what runs on the Sticher
##Easyiest way to keep Stitcher.py unaltered and to
##simultaniously handle multiple leyers of contours
import json
import os


##getting current dir
owd = os.getcwd()
os.chdir(owd)

with open('main.json', 'r') as settings:
    data = settings.read()
Data = json.loads(data)


tmp ={"Stitches3D" : [{}]} ##impose that Stitches3D is a list, otherwise
                            ## it becomes a object, i.e., becomes {}

##getting set up infos
FileDir = Data["FileDir"]
OutputDir = Data["OutputDir"]
DisplayConsoleStats = Data["DisplayConsoleStats"]
SaveFigureAutomatic = Data["SaveFigureAutomatic"] ##NOT WORKING!!!
MeshObjOutput = Data["MeshObjOutput"]

##tmp will be a temporary file used to execute Stitches.py
## properly. It's deleted at end.
tmp["FileDir"] = FileDir
tmp["OutputDir"] = OutputDir
tmp["DisplayConsoleStats"] = DisplayConsoleStats
tmp["SaveFigureAutomatic"] = SaveFigureAutomatic
tmp["MeshObjOutput"] = MeshObjOutput


##Manual loop
##Needed to properly handle the import Stitcher
##python will always execute any code that is written in the imported file
##unless it's only def
tmp["OBJFileName"] = "mesh0.obj"
tmp["Stitches3D"][0] = Data["Stitches3D"][0]
print(Data["Stitches3D"][0])
output = open("tmp.json","w")
json.dump(tmp,output)

output.close()
import Stitcher
os.chdir(owd)
os.remove("tmp.json")

##loop over all stitches
for i in range(1,len(Data["Stitches3D"])):
    os.chdir(owd)
    with open('main.json', 'r') as settings:
        data = settings.read()
    Data = json.loads(data)
    tmp["FileDir"] = FileDir
    tmp["OutputDir"] = OutputDir
    tmp["DisplayConsoleStats"] = DisplayConsoleStats
    tmp["SaveFigureAutomatic"] = SaveFigureAutomatic
    tmp["MeshObjOutput"] = MeshObjOutput
    tmp["OBJFileName"] = "mesh"+str(i)+".obj"
    tmp["Stitches3D"][0] = Data["Stitches3D"][i]
    print(Data["Stitches3D"][i])
    output = open("tmp.json","w")
    json.dump(tmp,output)
    output.close()
    exec(open("Stitcher.py").read())
    os.chdir(owd)
    os.remove("tmp.json")

print("Done")
