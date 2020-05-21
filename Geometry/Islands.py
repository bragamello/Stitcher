import numpy as np
import Proc.PointElement as PointElement
import Path.Cost as Cost

def IslandsEnsemble(I1x, I1y, I2x, I2y):

    ## Dump the position info into a class
    #I2x = I1x
    #I2y = I1y
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
