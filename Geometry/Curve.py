import numpy as np
import Proc.PointElement as PointElement
import Path.Cost as Cost
import Geometry.DistanceCheck as DistanceCheck


def CClockWise(Upperx,Uppery,Upperz):
    ## Reorients all surfaces to be counter-clockwise
    upperAreax = [0,0] ##first number is the acctual value and the second one is the sign
                        ## 0 means positive and 1 means negative
    upperAreay = [0,0]
    upperAreaz = [0,0]



    for i in range(0,len(Upperx)-1):
        upperAreax[0] += Uppery[i]*Upperz[i+1] - Upperz[i]*Uppery[i+1]
        upperAreay[0] += Upperz[i]*Upperx[i+1] - Upperx[i]*Upperz[i+1]
        upperAreaz[0] += Upperx[i]*Uppery[i+1] - Uppery[i]*Upperx[i+1]



    if upperAreax[0] > 0:
        upperAreax[1] = 0
    else:
        upperAreax[1] = 1
    if upperAreay[0] > 0:
        upperAreay[1] = 0
    else:
        upperAreay[1] = 1
    if upperAreaz[0] > 0:
        upperAreaz[1] = 0
    else:
        upperAreaz[1] = 1


#    print(upperAreax[0],upperAreay[0],upperAreaz[0])
#    print(upperAreax[1],upperAreay[1],upperAreaz[1])
#    print(lowerAreax[0],lowerAreay[0],lowerAreaz[0])
#    print(lowerAreax[1],lowerAreay[1],lowerAreaz[1])



    upperAreax[0] = np.absolute(upperAreax[0])
    upperAreay[0] = np.absolute(upperAreay[0])
    upperAreaz[0] = np.absolute(upperAreaz[0])


    ##Keeping the only relevant value
    ##Considering that we already know that
    ##both upper and lower surfaces have their
    ##orientation parallel to one of the axis (x, y or z)

    uppervalue = 0
    lowervalue = 0
    Orientation = 0 ##0 means Upper/Lower x, 1 Upper/Lower y
                    ##and 2 Upper/Lower z

    if upperAreax[0] > upperAreay[0]:
        if upperAreax[0] > upperAreaz[0]:
            uppervalue = upperAreax[1]
            Orientation = 0
        else:
            uppervalue = upperAreaz[1]
            Orientation = 2
    else:
        if upperAreay[0] > upperAreaz[0]:
            uppervalue = upperAreay[1]
            Orientation =  1
        else:
            uppervalue = upperAreaz[1]
            Orientation = 2



#    print(upperAreax[0],upperAreay[0],upperAreaz[0])
#    print(upperAreax[1],upperAreay[1],upperAreaz[1])
#    print(lowerAreax[0],lowerAreay[0],lowerAreaz[0])
#    print(lowerAreax[1],lowerAreay[1],lowerAreaz[1])

#    print(uppervalue)
#    print(lowervalue)


    if uppervalue == 1:
    	Upperx = list(reversed(Upperx))
    	Uppery = list(reversed(Uppery))
    	Upperz = list(reversed(Upperz))



    return Upperx,Uppery,Upperz, Orientation

def Thickness(Upperx,Uppery,Upperz, Lowerx,Lowery,Lowerz, Orientation):
    ## NOT BEING USED

    ## Calculates the thickness of two given slices in any orientation
    if Orientation == 0:
        return Upperx[0]-Lowerx[0]
    if Orientation ==1:
        return Uppery[0]-Lowery[0]
    if Orientation == 2:
        return Upperz[0]-Lowerz[0]
    return 0

def Orientation():

    return ori


def IslandsEnsemble(I1x, I1y, I2x, I2y):
    ## Caculates best point to connect two contours contained in the
    ## same slice

    test = 0
    M = int(len(I1x))
    I1 = [PointElement.Point]*(M)
    for i in range(0,M):
    	I1[i] = PointElement.Point(I1x[i],I1y[i]);

    N = int(len(I2x))
    I2 = [PointElement.Point]*(N)
    for i in range(0,N):
    	I2[i] = PointElement.Point(I2x[i]+test,I2y[i]+test);


    ConexionCord = Cost.DistanceMatrix(I1,I2)

    vari = M+N
    Final = [PointElement.Point]*(vari)
    m = 0
    n = ConexionCord[1]
    mc = 0
    nc = 0
    while mc<M:
        Final[mc+nc] = PointElement.Point(I1x[m],I1y[m])
        if m == ConexionCord[0]:
            while nc<N-1:
                Final[mc+nc] = PointElement.Point(I2x[n]+test,I2y[n]+test)
                n += 1
                nc += 1
                if n == N:
                    n = 0

            Final[mc+nc] = PointElement.Point(I2x[ConexionCord[1]]+test,I2y[ConexionCord[1]]+test)
            Final[mc+nc + 1] = PointElement.Point(I1x[ConexionCord[0]-1],I1y[ConexionCord[0]-1])
            m += 0
            mc += 1

        m += 1
        mc += 1
        if m == M:
            m = 0

    Final[vari-1] = PointElement.Point(I1x[len(I1x)-2],I1y[len(I1x)-2])



    return Final
