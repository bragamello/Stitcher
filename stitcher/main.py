import json
import numpy as np
import os
import reconstruction as rct
from file_reader import roiread

'''
    A colections of points Point() are correlated in a manner that creates
    a perimeter Perimeter(). Every perimeter should be nice, i.e.:
        1) Not self-intersecting;
        2) No overlaping points;
        3) Have a prefered orientation.
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


print("Loading files\n\n")
print(FileDir)

def island_init(file_dir,f,subdivision=3):
    arq = roiread(file_dir+"/"+f)
    I = rct.Perimeter(arq)
    I.remove_overlap()
    I.remove_overlap()
    I.fix_intersection()
    I.fix_distance(subdivision=3)
    I.c_clockwise()
    return I

for block in Data["Stitches3D"]:
    for section in block:
        S = rct.Surface()
        for file in block[section]:
            try:
                if isinstance(file,list):
                    I = 0
                    for f in file:
                        I_s = island_init(FileDir,f,3)
                        if I == 0:
                            I = I_s
                        else:
                            I.islands_ensemble(I_s)
                else:
                    I = island_init(FileDir,file,3)
                S.add_island(I)
            except Exception:
                print("Failed to load"+file)

        print("\nBuilding surface: ",section)
        S.build_surface()

        with open("Kamilla_interna_teste2628_"+section+".obj", "w") as out_file:
            out_file.write(S.surfaceV)
            out_file.write(S.surfaceE)
