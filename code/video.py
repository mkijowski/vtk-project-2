from __future__ import print_function
import numpy as np
import cv2 as cv
import argparse
import vtk

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='/home/mkijowski/videos/VASTChallenge2009-M3-VIDEOPART1.mov')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

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
  # ... set background color to white ...
  renderer.SetBackground(1, 1, 1)
  # ... and set window size.
  renderWin.SetSize(400, 400)

  renderInteractor.Initialize()
  # Because nothing will be rendered without any input, we order the first render manually before control is handed over to the main-loop.
  renderWin.Render()
  renderInteractor.Start()

def fromVid2Vtk(args):
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
    
    squash1 = np.swapaxes(np.stack(video, axis=-1),2,3)
    squash = np.ascontiguousarray(squash1, dtype=np.uint8)
    #data_string = squash.tostring()

    importer = vtk.vtkImageImport()
    importer.SetDataSpacing( 1, 1, 1 )
    importer.SetDataOrigin( 0, 0, 0 )

    importer.SetWholeExtent( 0, cols - 1 , 0, rows - 1, 0, length-1 )
    importer.SetDataExtentToWholeExtent()
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents (channels)
    #importer.CopyImportVoidPointer(data_string, len(data_string))
    importer.SetImportVoidPointer( squash )
    importer.Update()
    return importer.GetOutputPort()

if __name__ == '__main__':
    main()

