from __future__ import print_function
import numpy as np
import cv2 as cv
import argparse
import vtk
import sys
import os

sys.path.append(os.path.abspath("/home/mkijowski/git/vtk-project-2/libs"))
import numpy_support


parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='/home/mkijowski/videos/VASTChallenge2009-M3-VIDEOPART1.mov')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

def main():

  alphaChannelFunc = vtk.vtkPiecewiseFunction()
  alphaChannelFunc.AddPoint(0, 0.0)

  volumeProperty = vtk.vtkVolumeProperty()
  volumeProperty.SetScalarOpacity(alphaChannelFunc)

  #compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
  #compositeFunction = vtk.vtkFixedPointVolumeRayCastCompositeFunction()

  volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
  #volumeMapper.SetVolumeRayCastFunction(compositeFunction)
  volumeMapper.SetInputConnection(fromVid2Mat(args))

  volume = vtk.vtkVolume()
  volume.SetMapper(volumeMapper)
  volume.SetProperty(volumeProperty)

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
  renderInteractor.Initialize()
  # Because nothing will be rendered without any input, we order the first render manually before control is handed over to the main-loop.
  renderWin.Render()
  renderInteractor.Start()


def toms_main():

  img = cv.imread (inputFilename, cv.IMREAD_COLOR)

  # Create an actor
  actor = vtk.vtkImageActor()
  actor.GetMapper().SetInputData(fromMat2Vtk (img))

  # Setup renderer
  colors = vtk.vtkNamedColors()

  renderer = vtk.vtkRenderer()
  renderer.AddActor(actor)
  renderer.ResetCamera()
  #renderer.SetBackground(colors.GetColor3d("Burlywood").GetData())

  # Setup render window
  window = vtk.vtkRenderWindow()
  window.AddRenderer(renderer)

  # Setup render window interactor
  interactor = vtk.vtkRenderWindowInteractor()
  interactor.SetRenderWindow(window)

  # Setup interactor style (this is what implements the zooming, panning and brightness adjustment functionality)
  style = vtk.vtkInteractorStyleImage()
  interactor.SetInteractorStyle(style)

  # Render and start interaction
  interactor.Start()


def fromVid2Mat(args):
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
        ret, frame = capture.read()
        if frame is None:
            break

        #volume = vtkImageData()
        #volume.SetExtent((0, cols - 1, 0, rows - 1, 0, length - 1))

        #ncells = volume.GetNumberOfCells()
        #npoints = volume.GetNumberOfPoints()
        #array = vtkUnsignedShortArray()
        #array.SetNumberOfValues(npoints)
        blur_frame = cv.GaussianBlur(cv.bilateralFilter(frame,9,75,75),(5,5),0)
        fgBlurMask = backSub.apply(blur_frame)
        img_fg = cv.bitwise_and(frame, frame, mask = fgBlurMask)

        video.append(img_fg)

    squash = np.stack(video, axis=-1)
    return fromMat2Vtk(squash)

"""This content is for my attempt at loading the images in a vtk array
# per http://vtk.1045678.n5.nabble.com/reconstruct-a-stack-of-TIFF-images-in-3D-td5719585.html
"""
"""
          vals = img.GetPointData().GetAbstractArray('scalars')
# below is not working, cannot enumerate vals...?
          for i,v in enumerate(vals):
            array.SetValue(offset+i,v)

# Finally we have to assign our array to the volume image.
          volume.GetPointData().SetArray(array)


          keyboard = cv.waitKey(1)
          if keyboard == 'q' or keyboard == 27:
            break
"""
def fromMat2Vtk(opencv_src_img):
    importer = vtk.vtkImageImport()
    importer.SetDataSpacing( 1, 1, 1 )
    importer.SetDataOrigin( 0, 0, 0 )

    frame = cv.cvtColor( opencv_src_img, cv.COLOR_BGR2RGB)
    rows,cols,channels = frame.shape

    importer.SetWholeExtent( 0, cols - 1 , 0, rows - 1, 0, 0 )
    importer.SetDataExtentToWholeExtent()
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents (channels)
    importer.SetImportVoidPointer( frame )
    importer.Update()
    return importer.GetOutputPort()

if __name__ == '__main__':
    main()

