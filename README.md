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


### Building the singularity container
The build file for this project is [`opencv.build`](../master/opencv.build).
This build file uses the same VTK installation as my previous project and
expands it to build OpenCV version 4.1.0 from source.  
Note: This can take quite a while...  To build:
```
sudo singularity build ~/opencv-vtk.simg ./opencv.build
```

### Viewing Background subtraction
The initial work with background subtraction can be found here [`./code/bg-subtraction/`](../master/code/bg-subtraction/).
To test the background subtraction algorithm (inside the container):
```
singularity exec ~/opencv-vtk.simg python ./code/bg-subtraction/bg.py --input ./videos/april-18.mp4
```

#### Pre-processing with OpenCV
The bulk of the work being done to remove background data is performed by the
MOG2 background subtractor.  MOG2 is a Gaussian Mixture-based
Background/Foreground Segmentation Algorithm based on two papers authored by
Zoran Zivkovic. [1](http://www.zoranz.net/Publications/zivkovicPRL2006.pdf) [2](http://www.zoranz.net/Publications/zivkovic2004ICPR.pdf)

By tweaking some of the defaults I have obtained a
fairly good foreground mask with the following MOG2 parameters:
```
backSub = cv.createBackgroundSubtractorMOG2()
backsub.setHistory(300)
backsub.setVarThreshold(100)
backsub.setDetectShadows(1)
backSub.setComplexityReductionThreshold(.1)
backSub.setVarThresholdGen(5)
backSub.setVarMax(75)
backSub.setVarMin(4)
backSub.setVarInit(15)
```

The above is applied to each frame and creates a mask that separates moving
objects which it consideres part of the foreground from stationary objects which
it consideres part of the background.  The resulting output is called a mask,
which is an 8-bit frame that identifies the background as black and the
foreground as white.

Before applying the MOG2 I first apply a blurring algorithm to the image data.  
This reduces some noise in the resulting mask.  The two algorithms used to blur
the data are a GaussianBlur to reduce random noise, adn a bilateral filter to
sharpen some of the edges.

Finally, the mask is applied to the resulting blurred frame.  This mask can then
be bitwise anded with the original frame image to produce jus the foreground
segment with original color.

The plan from here on out is to load these foreground images into vtk and render
them as a simple cube with the black background rendered as transparent.

#### Importing into VTK
##### `numpy_support` in VTK
Attempting to implement a stackoverflow post of pseudocode by gstevo. [3](https://stackoverflow.com/questions/35965273/load-sequence-of-pngs-into-vtkimagedata-for-3d-volume-render-using-python)
```
import vtk
from vtk.util import numpy_support

pngfiles = glob.glob('*.png')

png_reader = vtk.vtkPNGReader()
png_reader.SetFileName(pngfiles[0])
x,y = png_reader.GetOutput().GetDimensions()

data_3d = np.zeros([x,y,len(pngfiles)])

for i,p in enumerate(png):
    png_reader.SetFileName(pngfiles[0])
    png_reader.Update()
    img_data = png_reader.GetOutput()
    data_3D[:,:,i] = numpy_support.vtk_to_numpy(img_data)

#save your 3D numpy array out.
data_3Dvtk = numpy_support.numpy_to_vtk(data_3D)
```
The crux of this attempt relied on a vtk utility called `numpy_support`
that was deprecated at some point.  I found the github repo containing these
utilities and attempted to import them into my modern vtk without success.

#### `vtkImageSlice` and `vtkImageStack`
A good amount of time was spent trying to implement these methods as they seemed
promising.  Unfortunately I was never able to figure out quite how to implement
them, also my next attempt seemed more promising.

#### numpy array manipulation
My last attempt seemed the most promising.  Instead of converting each frame to
vtk data I instead tried to concatenate each frame into one array and and pass
that to the provided `fromMat2VTK` function.

This method provided a good learning experience since it can be tested in python
interactively which helped with my understanding of the underlying data.  But I
was still not able to get the data into a vtkImageData format.


### Links
[MedicalDemo4](https://lorensen.github.io/VTKExamples/site/Python/Medical/MedicalDemo4/)

[Kwiver - kitware](https://github.com/Kitware/kwiver)

[vivia - kitware](https://github.com/Kitware/vivia)
