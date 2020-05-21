import numpy as np
import json
from math import *
tmp ={}

def Point(i,t):
    pointstring = "[0,0,0]"
    y = cos((2*pi*t)/3 + (i)*((2*pi)/10))
    z = sin((2*pi*t)/3 + (i)*((2*pi)/10))
    pointstring = "["+str(i)+","+str(y)+","+str(z)+"]"
    
    return pointstring

for i in range(0,100):
    output = open("hexagon"+str(i+1)+".json","w")
    tmp["ROI3DPoints"]=[Point(i,0),
                        Point(i,1),
                        Point(i,2)]
    json.dump(tmp,output)
    output.close()

