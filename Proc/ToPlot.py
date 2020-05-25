import numpy as np
import Proc.PointElement as PointElement

def Reshape(pointMatrix, remove_last = False):
    ##From class PointElement to regular x and y coord in python
    LEN = len(pointMatrix)
    x = np.zeros((LEN,1))
    y = np.zeros((LEN,1))
    for i in range(0,LEN):
        x[i] = float(pointMatrix[i].x)
        y[i] = float(pointMatrix[i].y)

    if remove_last:
        x=x[:-1]
        y=y[:-1]

    return np.array((x,y))


def PathCoord(path, upperPoints, lowerPoints, finalMinCord, Thickness):

    upper = ReshapeLastOut(upperPoints)
    lower = ReshapeLastOut(lowerPoints)
    auxUpper = np.zeros((2,len(upper[0])))
    auxLower = np.zeros((2,len(lower[0])))
    howManyM = 0
    howManyN = 0

    for i in range(0,len(upper[0])):

        if i+finalMinCord[0] < len(upper[0]):

            auxUpper[0][i] = upper[0][i + finalMinCord[0]]
            auxUpper[1][i] = upper[1][i + finalMinCord[0]]
            howManyM = i

        else:

            auxUpper[0][i] = upper[0][i - howManyM - 1]
            auxUpper[1][i] = upper[1][i - howManyM - 1]

    for i in range(0,len(lower[0])):

        if i+finalMinCord[1] < len(lower[0]):

            auxLower[0][i] = lower[0][i + finalMinCord[1]]
            auxLower[1][i] = lower[1][i + finalMinCord[1]]
            howManyN = i

        else:
            auxLower[0][i] = lower[0][i-howManyN-1]
            auxLower[1][i] = lower[1][i-howManyN-1]


        upper = auxUpper
        lower = auxLower

    Contour = np.zeros((2*len(path)+2,3))
    Contour[1] = [upper[0][0],upper[1][0],Thickness]
    Contour[0] = [lower[0][0],lower[1][0],    0    ]

    for i in range(0,len(path)):
        
        pathValueUpper = path[i][0]
        pathValueLower = path[i][1]
        Contour[2*i+3] = [upper[0][pathValueUpper],upper[1][pathValueUpper],Thickness]
        Contour[2*i+2] = [lower[0][pathValueLower],lower[1][pathValueLower],    0    ]


    return Contour
