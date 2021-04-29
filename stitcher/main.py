import json
import numpy as np
import os
import reconstruction as rct

def ROIRead(name):

    with open(name, 'r') as ROI:
        data = ROI.read()
        Data = json.loads(data)

    ## this parses OsiriX roi output into float numbers
    ## in x and y coordinate system
    copy = False
    j = 0
    number = ["","",""]
    ContourLength = len(Data["ROI3DPoints"])
    ROIPoints = np.array([[0.,0.,0.]]*(ContourLength + 1))

    ## litle loop to remove charecters from the midle of the numbers
    ## may just skip it
    ## Should check if .isnumeric() runs faster than True or False loop
    for i in range(0,ContourLength):
        for K in Data["ROI3DPoints"][i]:
            if copy and K != "," and K != "]":
            	number[j] = number[j] + K
            if K == "[":
            	copy = True
            if K == "]":
            	copy = False
            	j = 0
            if K == ",":
            	j += 1


        ROIPoints[i,0] = float(number[0])
        ROIPoints[i,1] = float(number[1])
        ROIPoints[i,2] = float(number[2])

        number = ["","",""]

    ## Repeting the first to point at the end
    ## of the array to create a closed curve
    ROIPoints[ContourLength] = ROIPoints[0]
    return ROIPoints

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
