from __future__ import print_function
import numpy as np
import cv2 as cv
import argparse
import vtk


def vismain(squash,rows,cols,channels,length):

  #alphaChannelFunc = vtk.vtkPiecewiseFunction()
  #alphaChannelFunc.AddPoint(0, 0.0)

  #volumeProperty = vtk.vtkVolumeProperty()
  #volumeProperty.SetScalarOpacity(alphaChannelFunc)

  volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
  volumeMapper.SetInputConnection(fromMat2Vtk(squash,rows,cols,channels,length))
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
  # ... set background color to white ...
  renderer.SetBackground(1, 1, 1)
  # ... and set window size.
  renderWin.SetSize(1000, 1000)

  renderWin.AddObserver("AbortCheckEvent", exitCheck)

  renderInteractor.Initialize()
  # Because nothing will be rendered without any input, we order the first render manually before control is handed over to the main-loop.
  renderWin.Render()
  renderInteractor.Start()

def fromVid2Mat(args):
    backSub = cv.createBackgroundSubtractorMOG2()
    backSub.setHistory(300)
    backSub.setVarThreshold(100)
    backSub.setDetectShadows(1)
    backSub.setComplexityReductionThreshold(.1)
    backSub.setVarThresholdGen(5)
    backSub.setVarMax(75)
    backSub.setVarMin(4)
    backSub.setVarInit(15)

    capture = cv.VideoCapture(cv.samples.findFileOrKeep(args))
    if not capture.isOpened:
        print('Unable to open: ' + args.input)
        exit(0)

    ### Load first frame to get shapes
    ret, frame = capture.read()
    length = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
    rows,cols,channels = frame.shape
    video = []
    
    ### Load video and apply mask
    while True:
        if frame is None:
            break
        blur_frame = cv.GaussianBlur(cv.bilateralFilter(frame,9,75,75),(5,5),0)
        fgBlurMask = backSub.apply(blur_frame)
        img_fg = cv.bitwise_and(frame, frame, mask = fgBlurMask)
        rgb_img_fg = cv.cvtColor( img_fg, cv.COLOR_BGR2RGB)
        video.append(rgb_img_fg)
        ret, frame = capture.read()
    
    squash = np.swapaxes(np.stack(video, axis=-1),2,3)
    
    return squash
    
def fromMat2Vtk(squash,rows,cols,channels,length):
    data_string = squash.tostring()

    importer = vtk.vtkImageImport()
    importer.SetDataSpacing( 1, 1, 1 )
    importer.SetDataOrigin( 0, 0, 0 )

    importer.SetWholeExtent( 0, cols - 1 , 0, rows - 1, 0, length-1 )
    importer.SetDataExtentToWholeExtent()
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents (channels)
    #importer.CopyImportVoidPointer(data_string, len(data_string))
    importer.SetImportVoidPointer( data_string )
    importer.Update()
    return importer.GetOutputPort()

def exitCheck(obj, event):
    if obj.GetEventPending() != 0:
        obj.SetAbortRender(1)


