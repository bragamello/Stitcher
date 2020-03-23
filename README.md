# Stitcher
Reconstruction of 3D Surfaces

# Introduction

  Based on ___ ,  we developed a code that could reconstruct a 3D surface given 2D plannar contours to start from. The idea is to connect M points in a plane to N points on another plane in the most parsimonious way possible, wich is accomplishable by minimizing the total length of the connection lines. On the process of doing so, the program can also connect contours that belong to a same plane by making conecting their nearest points.
  A few tools have also been used to improve the final surface such as:
  
      . Artificially improving the resolution by interpolating the coeficients of the Fourier's Series of each contour;
      . Auto-selection of files(Not fully implemented);
      . Etc
  
  More text
  

# Libraries Used

    . Numpy
    . Matplotlib
    . Scipy
    . Scikit-Image

# The Input

  Description of the main.json file

# The Output
  
  The program outputs the number of inputed files minus 1. Each output file contaning Verticies and Edges organized in a format that is readable, for example, in [Meshlab](http://www.meshlab.net).
