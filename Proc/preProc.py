import numpy as np
import Proc.PointElement as PointElement
import Proc.OpenROI as OpenROI
import Geometry.Curve as Curve
import Geometry.DistanceCheck as DistanceCheck
import Geometry.Islands as Islands

def preProc(*Names, DispConsole = False, resolution = 0.8):

    if len(Names) > 1:
        File1Name = Names[0]
        File1Name2 = Names[1]

        ## Input .json file. Brain slices
        I1x,I1y,I1z = OpenROI.ROIRead(File1Name)
        I2x,I2y,I2z = OpenROI.ROIRead(File1Name2)
        Thickness = I1z[0] - I2z[0]

        ## The orientation of the curve must be the same on both
        ## contours. The FixOrientation function corrects the orientation
        I1x,I1y,I1z,Orientation = Curve.CClockWise(I1x,I1y,I1z)
        I2x,I2y,I2z,Orientation = Curve.CClockWise(I2x,I2y,I2z)

        ##Checks and fixes points that are too spread out apart
        ##filling the gaps with on a linear fashion

        if Orientation == 0:
        	Island1x,Island1y,Island1z = DistanceCheck.FixPoints(I1y,I1z,I1x,resolution)
        	Island2x,Island2y,Island2z = DistanceCheck.FixPoints(I2y,I2z,I2x,resolution)
        if Orientation == 1:
        	Island1x,Island1y,Island1z = DistanceCheck.FixPoints(I1z,I1x,I1y,resolution)
        	Island2x,Island2y,Island2z = DistanceCheck.FixPoints(I2z,I2x,Iy2,resolution)
        if Orientation == 2:
        	Island1x,Island1y,Island1z = DistanceCheck.FixPoints(I1x,I1y,I1z,resolution)
        	Island2x,Island2y,Island2z = DistanceCheck.FixPoints(I2x,I2y,I2z,resolution)


        Slice = Curve.IslandsEnsemble(Island1x, Island1y, Island2x, Island2y, Thickness)
        M = len(Slice)
        Slicex = [0]*M
        Slicey = [0]*M
        Slicez = Island1z
        Slicez.append(Island2z)
        for i in range(0,M):
        	Slicex[i] = Slice[i].x;
        	Slicey[i] = Slice[i].y;

        if len(Names)>2:
            j = 0
            for i in range(2,len(Names)-1):
                File1Name2 = Names[j+1]
                I2x,I2y,I2z = OpenROI.ROIRead(File1Name2)
                I2x,I2y,I2z,Orientation = Curve.CClockWise(I2x,I2y,I2z)
                if Orientation == 0:
                	Island2x,Island2y,Island2z = DistanceCheck.FixPoints(I2y,I2z,I2x,resolution)
                if Orientation == 1:
                	Island2x,Island2y,Island2z = DistanceCheck.FixPoints(I2z,I2x,Iy2,resolution)
                if Orientation == 2:
                	Island2x,Island2y,Island2z = DistanceCheck.FixPoints(I2x,I2y,I2z,resolution)
                Slice = Curve.IslandsEnsemble(Slicex, Slicey, Island2x, Island2y, Thickness)
                M = len(Slice)
                Slicex = [0]*M
                Slicey = [0]*M
                Slicez.append(Island2z)
                for i in range(0,M):
                	Slicex[i] = Slice[i].x;
                	Slicey[i] = Slice[i].y;
                j += 1

    else:
        File1Name = Names[0]

        ## Input .json file. Brain slices

        I1x,I1y,I1z = OpenROI.ROIRead(File1Name)

        ## The orientation of the curve must be the same on both
        ## contours. The FixOrientation function corrects the orientation
        if DispConsole:
        	print("Checking Curve Orientation...")

        I1x,I1y,I1z,Orientation = Curve.CClockWise(I1x,I1y,I1z)


        if DispConsole:
        	print("All Curves setted to counter clock-wise.")

        ##Checks and fixes points that are too spread out apart
        ##filling the gaps with on a linear fashion
        if DispConsole:
        	print("Checking for large gaps...")
        if Orientation == 0:
        	Island1x,Island1y,Island1z = DistanceCheck.FixPoints(I1y,I1z,I1x,resolution)
        if Orientation == 1:
        	Island1x,Island1y,Island1z = DistanceCheck.FixPoints(I1z,I1x,I1y,resolution)
        if Orientation == 2:
        	Island1x,Island1y,Island1z = DistanceCheck.FixPoints(I1x,I1y,I1z,resolution)

        Slicex = Island1x
        Slicey = Island1y
        Slicez = Island1z

        if DispConsole:
        	if len(Island1x) != len(I1x):
        		print("Gaps fixed!")
        	else:
        		print("There was no large gap.")

        N = len(Slicex)
        Slice = [PointElement.Point]*N
        for i in range(0,N):
        	Slice[i] = PointElement.Point(Island1x[i],Island1y[i]);

    return Slicex,Slicey,Slicez, Slice, Orientation
