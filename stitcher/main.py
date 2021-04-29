import json
import numpy as np
import os
import reconstruction as rct
import file_reader.ROIRead as ROIRead

with open('main.json', 'r') as settings:
    data = settings.read()
Data = json.loads(data)
FileDir = Data["FileDir"]
OutputDir = Data["OutputDir"]
DisplayConsoleStats = Data["DisplayConsoleStats"]
MeshObjOutput = Data["MeshObjOutput"]

S = rct.Surface()
print("Loading files\n\n")
print(FileDir)

for block in Data["Stitches3D"]:
    for section in block:
        for file in block[section]:
            print(file)
            arq = ROIRead(FileDir+"/"+file)
            I = rct.Perimeter(arq)
            I.remove_overlap()
            I.fix_distance()
            I.fix_intersection()
            I.c_clockwise()
            S.add_island(I)

print("\nBuilding surface")
S.build_surface()

with open("inter_RH_PIAL_2.obj", "w") as out_file:
    out_file.write(S.surfaceV)
    out_file.write(S.surfaceE)
if 0:
    with open("main_RH_PIAL_.json", "w") as file:
        for i in range(1,40):
            test = json.dumps(str(i)+"_rh_pial.json")
            file.write(test+",")
