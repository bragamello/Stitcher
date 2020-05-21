import numpy as np
import math
import random

def Distance(P1, P2, Thickness):
	## distance between 2 points in the case of
	## - Rough Cost Matrix
	## - used to select the first connection
	return  math.sqrt((P1.x - P2.x) ** 2 + (P1.y - P2.y) ** 2 + Thickness ** 2)

def DistanceMatrix(Upper,Lower):
	## Upper stands for the surface on top and Lower for the one in the bottom
	M = len(Upper);
	N = len(Lower);

	distMatrix = np.zeros((M-1,N-1))
	for m in range(0,M-1):
		for n in range(0,N-1):
			distMatrix[m,n] = Distance(Upper[m],Lower[n],1) ##Wacht out!!

	## finding all min values contained inthe matrix
	## There's usually only one, but the value might be repeated somewhere
	allMin = np.where(distMatrix == np.amin(distMatrix))
	listOfCordinates = list(zip(allMin[0], allMin[1]))

	finalMinCord = listOfCordinates[0] ## getting the first cuz why not
	##finalMinCord will be the value used to rearange the matrix
	##considering the first element to be the one with maximum resembalnce
	##i.e., the one with minimal distance from the point above
	#print(distMatrix[finalMinCord[0],finalMinCord[1]])

	return finalMinCord

def CostMatrix(ReorderedUpper,ReorderedLower,Thickness):
	## Upper stands for the surface on top and Lower for the one in the bottom
	M = len(ReorderedUpper);
	N = len(ReorderedLower);

	costMatrix = np.zeros((M-1,N-1))
	for m in range(0,M-1):
		for n in range(0,N-1):
			costMatrix[m,n] = Distance(ReorderedUpper[m],ReorderedLower[n],Thickness)
	return costMatrix

def FindPath(FinalMatrix, M, N):
    M = M - 1
    N = N - 1

    oFinalMatrix = FinalMatrix;
    MinCost = np.zeros((M,N));
    MinCost[0][0] = FinalMatrix[0][0];

## setting the upper border cost
    for j in range(1,N):
        MinCost[0][j] = MinCost[0][j-1] + FinalMatrix[0][j];

## setting the left border cost
    for i in range(1,M):
        MinCost[i][0] = MinCost[i-1][0] + FinalMatrix[i][0];

    for i in range(1,M):
        for j in range(1,N):
            best = min(MinCost[i-1][j],MinCost[i][j-1])
##            if random.random()<=0.5:
##                    best = MinCost[i-1][j]
##            else:
##                    best = MinCost[i][j-1]
            MinCost[i][j] = best + FinalMatrix[i][j]
            if MinCost[i][j]<=0:
                    print("problem")

##every thing from now on is a way to find whats the acctual path
##not only the cost of getting there

    var1 = False
    var2 = False
    thePath = [0]*(M+N-2)
    thePath[M+N-3] = [M-1,N-1]
    m = M-1
    n = N-1
    for i in range(M+N-3,-1,-1):
        if m>0 and n>0:
            if MinCost[m-1][n] < MinCost[m][n-1]:
                m = m - 1
            else:
                n = n - 1
        else:
            if m<=0:
                n = n - 1
            else:
                m = m - 1

        index = M+N-i-3
        thePath[index] = [m,n]

        if [m,n] == [0,N-1]:
            var1 = True
        if [m,n] == [M-1,0]:
            var2 = True

##var1 and var2 are used to add a single point in order to make the
##the graph a closed cicle

    if var1:
        thePath.append([M-1,0])
        MinCost = MinCost + oFinalMatrix[M-1][0]
        return [MinCost,thePath]
    if var2:
        thePath.append([0,N-1])
        MinCost = MinCost + oFinalMatrix[0][N-1]
        return [MinCost,thePath]

    if oFinalMatrix[M-1][0]<oFinalMatrix[0][N-1]:
        thePath.append([M-1,0])
        MinCost = MinCost + oFinalMatrix[M-1][0]
        return [MinCost,thePath]
    else:
        thePath.append([0,N-1])
        MinCost = MinCost + oFinalMatrix[0][N-1]
        return [MinCost,thePath]
