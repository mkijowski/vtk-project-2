#!/usr/bin/python
import vtk
import cv2 as cv
import numpy as np

def fromMat2Vtk(src):
    importer = vtk.vtkImageImport()
    importer.SetDataSpacing( 1, 1, 1 )
    importer.SetDataOrigin( 0, 0, 0 )

    frame = cv.cvtColor( src, cv.COLOR_BGR2RGB)
    flipped = cv.flip(frame,0)
    rows,cols,channels = frame.shape

    importer.SetWholeExtent( 0, cols - 1 , 0, rows - 1, 0, 0 )
    importer.SetDataExtentToWholeExtent()
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents (channels)
    importer.SetImportVoidPointer( flipped )
    importer.Update()
    return importer.GetOutput()


def main():
  # Parse input arguments
  inputFilename = 'Bunny.jpg'

  img = cv.imread (inputFilename, cv.IMREAD_COLOR)

   # Read the image
  reader = vtk.vtkJPEGReader()
  reader.SetFileName(inputFilename)
  reader.Update()

  otherreader = vtk.vtkImageData()

  #fromMat2Vtk (input, otherreader)

  # Create an actor
  actor = vtk.vtkImageActor()
  #actor.GetMapper().SetInputConnection(reader.GetOutputPort())
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


if __name__ == '__main__':
    main()

