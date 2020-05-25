import numpy as np

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

## Write .OBJ file
## Meshlab readable output
def Vertices(Upper, Lower, Upperz, Lowerz):
    string = ""

    for i in range(0,len(Upper[0])-1):

        text =  "v " + str(float(Upper[0][i])) +\
                " " + str(float(Upper[1][i])) +\
                " " + str(Upperz) + "\n"

        string = string + text

    for i in range(0,len(Lower[0])-1):

        text =  "v " + str(float(Lower[0][i])) + " " +\
                str(float(Lower[1][i])) + " " +\
                str(Lowerz) + "\n"

        string = string + text

    return string

def Faces(thePath,M,N):
    string = ""
    thePath.insert(0,[M-1,N-1])

    for i in range(0,len(thePath)-1):

        if int(thePath[i][1]) == int(thePath[i+1][1]):

            text1 = "f " +str(int(thePath[i][0])+1) +\
                    " " + str(int(thePath[i][1])+1+M) +\
                    " " + str (int(thePath[i+1][0])+1) + "\n"

            string = string + text1

        else:

            text2 = "f " +str(int(thePath[i][1])+1+M) + \
                    " " + str(int(thePath[i+1][0])+1) + \
                    " " + str (int(thePath[i+1][1])+1+M) + "\n"

            string = string + text2

    if  int(thePath[len(thePath)-1][0])+1 == int(thePath[len(thePath)-1][1])+1+M or\
        int(thePath[len(thePath)-1][0])+1 == int(thePath[0][0])+1 or\
        int(thePath[0][0])+1 == int(thePath[len(thePath)-1][1])+1+M:

        string =    string + "f " +\
                    str(int(thePath[len(thePath)-1][1])+1+M) + " " +\
                    str(int(thePath[len(thePath)-1][0])+1) + " " +\
                    str (int(thePath[0][1])+1+M) + "\n"

    else:

        string =    string + "f " +\
                    str(int(thePath[len(thePath)-1][0])+1) + " " +\
                    str(int(thePath[len(thePath)-1][1])+1+M) + " " +\
                    str (int(thePath[0][0])+1) + "\n"

    return string
