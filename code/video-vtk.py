from __future__ import print_function
import cv2 as cv
import argparse
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='/home/mkijowski/videos/VASTChallenge2009-M3-VIDEOPART1.mov')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2(history=100,varThreshold=200,detectShadows=0)
    backSub.setComplexityReductionThreshold(.3)
    backSub.setVarThresholdGen(10)
    #backSub.setVarMax(75)
    #backSub.setVarMin(15)
    #backSub.setVarInit(20)
else:
    backSub = cv.createBackgroundSubtractorKNN(history=200,dist2Threshold=400,detectShadows=1)
    backSub.setkNNSamples(1)
    backSub.setNSamples(25)

capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    #blur_frame = cv.GaussianBlur(frame,(5, 5), 0)
    blur_frame = cv.medianBlur(frame,5)
    fgBlurMask = backSub.apply(blur_frame)
    fgMask = backSub.apply(frame)
    #varmax = backSub.getVarMin()
    #print(varmax)

    #cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    #cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
    #           cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))

    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    cv.imshow('Blur Frame', fgBlurMask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

def fromMat2Vtk(src):
    importer = vtk.vtkImageImport()
    importer.SetDataSpacing( 1, 1, 1 )
    importer.SetDataOrigin( 0, 0, 0 )

    frame = cv.cvtColor( src, cv.COLOR_BGR2RGB)
    rows,cols,channels = frame.shape

    importer.SetWholeExtent( 0, cols - 1 , 0, rows - 1, 0, 0 )
    importer.SetDataExtentToWholeExtent()
    importer.SetDataScalarTypeToUnsignedChar()
    importer.SetNumberOfScalarComponents (channels)
    importer.SetImportVoidPointer( frame )
    importer.Update()
    return importer.GetOutput()



