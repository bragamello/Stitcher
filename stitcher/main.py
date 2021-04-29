import json
import numpy as np
import os
import reconstruction as rct
import file_reader.roiread as roiread

'''
    A colections of points Point() are correlated in a manner that creates
    a perimeter Perimeter(). Every perimeter should be nice, i.e.:
        1) Not self-intersecting;
        2) No overlaping points;
        3) Have a prefered orientation
    If we can garantee this properties, than we proceed to stitch a colection
    of perimeters in a surface Surface().
'''
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
            arq = roiread(FileDir+"/"+file)
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
