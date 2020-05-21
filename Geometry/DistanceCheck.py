import math
import numpy as np
import Proc.PointElement as PointElement
import Proc.OpenROI as OpenROI

def FixPoints(x,y,z,resolution):
	counter = 0
	distance = [0]*len(x)
	finalx = [20*resolution]*len(x)
	finaly = [20*resolution]*len(x)
	finalz = z

	for i in range(0,len(x)-1):
		distance[i] = math.sqrt((x[i]-x[i+1])**2+(y[i]-y[i+1])**2)

	d0 = np.sum(distance)/(1.*len(x))
	aux = 0
	for i in range(0,len(x)-1):
		if np.absolute(distance[i]) >= (d0): ##3.0 is 100% arbitrary
			factor = int(distance[i]/d0)
			for j in range(1,factor):
				finalx.insert(i+j+counter , ((x[i]-x[i+1])*j/factor)+x[i+1])
				finaly.insert(i+j+counter , ((y[i]-y[i+1])*j/factor)+y[i+1])
				finalz.insert(i+j+counter ,             z[0]             )
				aux += 1
			counter += aux
			aux = 0



	counter = 0
	for i in range(0,len(finalx)):
		if finalx[i]==20*resolution:
			finalx[i] = x[counter]
			finaly[i] = y[counter]
			counter = counter + 1


	return finalx,finaly,finalz
