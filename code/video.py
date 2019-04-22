from __future__ import print_function
import numpy as np
import cv2 as cv
import argparse
import vtk

"""
Parse arguments for input and background subtraction algorithm.
--algo has not been tested with background subtractors other then MOG2.
Note: the default input file probably does not exist in the location specified.
"""
parser = argparse.ArgumentParser(description='This program uses background subtraction methods provided by \
                                              OpenCV and renders a volume in VTK consisting of the foreground \
                                              from each frame in the video.')
parser.add_argument('--input', type=str, help='Path to a video.', default='~/videos/VASTChallenge2009-M3-VIDEOPART1.mov')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

"""
Main method performs the setup of the VTK pipeline.
Nothing terribly complicated going on here...
"""
def main():

  #alphaChannelFunc = vtk.vtkPiecewiseFunction()
  #alphaChannelFunc.AddPoint(0, 0.0)

  #volumeProperty = vtk.vtkVolumeProperty()
  #volumeProperty.SetScalarOpacity(alphaChannelFunc)

  volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
  volumeMapper.SetInputConnection(fromVid2Vtk(args))
  volumeMapper.SetBlendModeToComposite()

  volume = vtk.vtkVolume()
  volume.SetMapper(volumeMapper)
  #volume.SetProperty(volumeProperty)
  volume.Update()

  renderer = vtk.vtkRenderer()
  renderWin = vtk.vtkRenderWindow()
  renderWin.AddRenderer(renderer)
  renderInteractor = vtk.vtkRenderWindowInteractor()
  renderInteractor.SetRenderWindow(renderWin)

  renderer.AddVolume(volume)
  renderer.SetBackground(1, 1, 1)
  renderWin.SetSize(400, 400)

  renderInteractor.Initialize()
  renderWin.Render()
  renderInteractor.Start()

"""
fromVid2VTK takes two arguments from ArgumentParser.
args.input is the path to the video file to use as input.
args.algo is the algorithm used for background subtraction.

fromVid2Vtk returns the OutputPort of a vtkImageImport algorithm.
This algorithm should contain each frame from the video after the background
has been subtracted.
"""
def fromVid2Vtk(args):
    ## Configure background subtractor
    if args.algo == 'MOG2':
        backSub = cv.createBackgroundSubtractorMOG2()
        backSub.setHistory(300)
        backSub.setVarThreshold(100)
        backSub.setDetectShadows(1)
        backSub.setComplexityReductionThreshold(.1)
        backSub.setVarThresholdGen(5)
        backSub.setVarMax(75)
        backSub.setVarMin(4)
        backSub.setVarInit(15)
    else:
        backSub = cv.createBackgroundSubtractorKNN(history=200,dist2Threshold=400,detectShadows=1)
        backSub.setkNNSamples(1)
        backSub.setNSamples(25)

    capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
    if not capture.isOpened:
        print('Unable to open: ' + args.input)
        exit(0)

    ### Load first frame to get some required data 
    ### Needed data are number of rows, columns (resolution of video)
    ### number of channels (probably 3 since most videos are color RGB)
    ### and length which is just the total number of frames in the video
    ret, frame = capture.read()
    length = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
    rows,cols,channels = frame.shape

    ### Create array to store each frame
    video = []

    ### Load video and apply background subtraction to generate mask
    ### and apply mask to original frame to get foreground
    ### Fix colors(BGR to RGB) and flip image to prepare data for VTK
    while True:
        if frame is None:
            break
        blur_frame = cv.GaussianBlur(cv.bilateralFilter(frame,9,75,75),(5,5),0)
        fgBlurMask = backSub.apply(blur_frame)
        img_fg = cv.bitwise_and(frame, frame, mask = fgBlurMask)
        rgb_img_fg = cv.cvtColor( img_fg, cv.COLOR_BGR2RGB)
        video.append(rgb_img_fg)
        ret, frame = capture.read()

    ### Stack the frames into one object, swap the 2 and 3 axes to prepare for VTK
    squash1 = np.swapaxes(np.stack(video, axis=-1),2,3)
    squash = np.ascontiguousarray(squash1, dtype=np.uint8)
    #data_string = squash.tostring()


    ### Create VTK image import and load frame data into it
    importer = vtk.vtkImageImport()
    importer.SetDataSpacing( 1, 1, 1 )
    importer.SetDataOrigin( 0, 0, 0 )

    importer.SetWholeExtent( 0, cols - 1 , 0, rows - 1, 0, length-2 )
    importer.SetDataExtentToWholeExtent()
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents (channels)
    #importer.CopyImportVoidPointer(data_string, len(data_string))
    importer.SetImportVoidPointer( squash )
    importer.Update()
    return importer.GetOutputPort()

# Run main()
if __name__ == '__main__':
    main()

