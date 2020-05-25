import numpy as np
import Proc.PointElement as PointElement
import Path.Cost as Cost
import Proc.preProc as preProc
import json
import os

### SETTINGS #####

with open('tmp.json', 'r') as settings:
    data = settings.read()
Data = json.loads(data)

FileDir = Data["FileDir"]
os.chdir(FileDir)

Slice1 = Data["Stitches3D"][0]["upper"]
Slice2 = Data["Stitches3D"][0]["lower"]


DisplayConsoleStats = Data["DisplayConsoleStats"] ##Choose True or False
Plotfigure = False
SaveFigureAutomatic = Data["SaveFigureAutomatic"] ##to be implemented
MeshObjOutput = Data["MeshObjOutput"]
OBJFileName = Data["OBJFileName"]
OutputDir = Data["OutputDir"]


##################


if DisplayConsoleStats:
	print("Processing upper contour")
Upperx, Uppery, Upperz, Upper, Orientation = preProc.preProc(*Slice1,DispConsole = DisplayConsoleStats)

if DisplayConsoleStats:
	print("\n\n")
	print("Processing lower contour")
Lowerx, Lowery, Lowerz, Lower, Orientation = preProc.preProc(*Slice2,DispConsole = DisplayConsoleStats)

if DisplayConsoleStats:
	print("\n")

## distance between slices:
Thickness = Upperz[0]-Lowerz[0]

if DisplayConsoleStats:
	print("Calculating the best stitch.")

## Choose the first conection
## Nearest upper/lower pair. (can insert other criteria)
finalMinCord = Cost.DistanceMatrix(Upper,Lower,Thickness)

## Re-order the points: put the first connection at (0,0)
## The Upper contour
M = len(Upperx)
ReorderedUpper = [PointElement.Point]*M

for i in range(0,M):

	if (i-finalMinCord[0]) >= 0:

		index = i-finalMinCord[0]
		ReorderedUpper[index] = PointElement.Point(Upperx[i],\
                                                Uppery[i])

	else:
		index = M-finalMinCord[0] + i - 1
		ReorderedUpper[index] = PointElement.Point(Upperx[i],\
                                                Uppery[i])

ReorderedUpper[M-1] = PointElement.Point(Upperx[finalMinCord[0]],\
                                        Uppery[finalMinCord[0]]
                                        )

## The Lower contour
N = len(Lowerx)
ReorderedLower = [PointElement.Point] * N

for i in range(0,N):

	if (i-finalMinCord[1]) >= 0:

		index = i - finalMinCord[1]
		ReorderedLower[index] = PointElement.Point(Lowerx[i],Lowery[i])
	else:

		index = N - finalMinCord[1] + i - 1
		ReorderedLower[index] = PointElement.Point(Lowerx[i],Lowery[i])

ReorderedLower[N-1] = PointElement.Point(Lowerx[finalMinCord[1]],\
                                        Lowery[finalMinCord[1]]
                                        )

## Calculate the cost matrix
costMatrix = Cost.CostMatrix(ReorderedUpper,\
                            ReorderedLower,\
                            Thickness
                            )

## Find the MinCost path
[MinCost,thePath] = Cost.FindPath(costMatrix, M, N)


if DisplayConsoleStats:

	print("Done!")


if MeshObjOutput:

	if DisplayConsoleStats:

		print("Creating .obj file.")

	import Proc.MeshObj as MeshObj
	os.chdir(OutputDir)

	## Output to Meshlab
	OBJfileOutput = open(OBJFileName,"w")

	## From class to regular np array
	ReorderedUpper = MeshObj.Reshape(ReorderedUpper)
	ReorderedLower = MeshObj.Reshape(ReorderedLower)

	## Messhlab readable output
	Vertices = MeshObj.Vertices(ReorderedUpper,\
                                ReorderedLower,\
                                Upperz[0],\
                                Lowerz[0]
                                )

	Faces = MeshObj.Faces(thePath,\
                        len(ReorderedUpper[0])-1,\
                        len(ReorderedLower[0])-1)

	OBJfileOutput.write(Vertices + Faces);

	if DisplayConsoleStats:
		print("Done!")



if Plotfigure:
	if DisplayConsoleStats:
		print("Plotting figure...")

	import matplotlib.pyplot as plt
	from mpl_toolkits.mplot3d import Axes3D
	import Proc.ToPlot as ToPlot

	os.chdir(Data["OutputDir"])
    ##Geting each line segment to be plot individually
	Contour = ToPlot.PathCoord(thePath, Upper, Lower, finalMinCord,Thickness)
	fig = plt.figure().add_subplot(111, projection='3d')

	Upper = ToPlot.Reshape(Upper)
	Lower = ToPlot.Reshape(Lower)

	x = np.zeros( (np.shape(Contour)[0]) )
	y = np.zeros( (np.shape(Contour)[0]) )
	z = np.zeros( (np.shape(Contour)[0]) )

	for i in range(0,np.shape(Contour)[0]):

	    x[i] = Contour[i][0]
	    y[i] = Contour[i][1]
	    z[i] = Contour[i][2]

	for i in range(0,int(np.shape(Contour)[0]/2)):

	    fig.plot3D([x[2*i],x[2*i+1]],[y[2*i],y[2*i+1]],[z[2*i],z[2*i+1]])

	fig.plot3D(Lower[0],Lower[1],0)
	fig.plot3D(Upper[0],Upper[1],Thickness)
	plt.axis("on")
	plt.show()
