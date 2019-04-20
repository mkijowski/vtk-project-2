### Project 2

#### Assignment
Develop a video visualization for the provided security video feeds. Before
the visualization step, preprocess the videosusing suitable steps to eliminate
as much unneeded information as possible for a cleaner final visualization.

#### Resources
* [VAST 2009 video
  1](http://avida.cs.wright.edu/courses/CEG7560/VASTChallenge2009-M3-VIDEOPART1.mov)
* [VAST 2009 video
  2](http://avida.cs.wright.edu/courses/CEG7560/VASTChallenge2009-M3-VIDEOPART2.mov)
* [Vast 2009
  challenge](https://www.cs.umd.edu/hcil/varepository/VAST%20Challenge%202009/challenges/MC3%20-%20Video%20Analysis/)
* [Cool Vast mini challenge
  video](https://www.vis.uni-stuttgart.de/forschung/visual_analytics/visuelle_analyse_videostroeme/vast_challenge_2009/index.html)
* Several smaller Nest camera videos for testing have been uploaded
  [here](../master/videos)

#### Starting point
My first steps for this project were to install OpenCV into my vtk container
from project 1.  You can find the Singularity container build file in this
repository [`opencv.build`](../master/opencv.build).

Next I began experimenting with basic background extraction samples available on the
[OpenCV documentation
site](https://docs.opencv.org/4.1.0/db/d5c/tutorial_py_bg_subtraction.html).
Initial attempts at background subtraction can be found here:
[`./code/bg-subtraction/`](../master/code/bg-subtraction/).



### Links
[Kwiver - kitware](https://github.com/Kitware/kwiver)
[vivia - kitware](https://github.com/Kitware/vivia)
https://docs.opencv.org/4.1.0/d6/da7/classcv_1_1bgsegm_1_1BackgroundSubtractorMOG.html

