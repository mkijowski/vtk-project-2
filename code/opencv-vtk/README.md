### Testing code
This directory contains test code for opening an image in opencv and importing
the resulting mat data into VTK.

The resulting vtk window should have a properly flipped image of bugs bunny with
the correct color scheme (converted OpenCV's BGR data to RGB for VTK).

Execute with `python ./opencv-vtk.py`
