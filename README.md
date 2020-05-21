# Stitcher
Reconstruction of 3D Surfaces

# Introduction

  Based on ___ ,  we developed a code that could reconstruct a 3D surface given 2D planar contours to start from. The idea is to connect M points in a plane to N points on another plane in the most parsimonious way possible, which is accomplish-able by minimizing the total length of the connection lines. On the process of doing so, the program can also connect contours that belong to a same plane by making connecting their nearest points.
  A few tools have also been used to improve the final surface such as:

      . Artificially improving the resolution by interpolating the coefficients of the Fourier's Series of each contour;
      . Auto-selection of files(Not fully implemented);
      . Etc

  More text


# Libraries Used

    . Numpy
    . Matplotlib
    . Scipy
    . Scikit-Image

# The Input

  Input files should be organized as:


  And one should also provide a file containing the order in which the islands should be connected, as the program can not yet decide it in a parsimonious way. This file should be structured as follows:

              {"Stitches3D": [
              {"upper": ["one.json"], "lower": ["two.json"]},
              {"upper": ["two.json", "three.json", "four.json"], "lower": ["five.json", "six.json"]},
              ],
              "FileDir": "/path/to/conturs/json",
              "OutputDir": "/path/to/out/put/mesh",
              "DisplayConsoleStats": BOOLEAN,
              "SaveFigureAutomatic": BOOLEAN,
              "MeshObjOutput": BOOLEAN}

  On this example, the first plane contains only one island which is only connected to the island 'two' in the second plane. The second plane however has 3 islands and all of them will be connected to islands five and six in the third plane.
  
# The Output

  The program outputs the number of inputed files minus 1. Each output file contaning Verticies and Edges organized in a format that is readable, for example, in [Meshlab](http://www.meshlab.net).
