from __future__ import print_function
import cv2 as cv
import argparse
import vtk

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='/home/mkijowski/videos/VASTChallenge2009-M3-VIDEOPART1.mov')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()


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

    ### Load video and apply mask
    while True:
        ret, frame = capture.read()
        if frame is None:
            break

        #blur_frame = cv.bilateralFilter(frame,9,75,75)
        blur_frame = cv.GaussianBlur(cv.bilateralFilter(frame,9,75,75),(5,5),0)
        #blur_frame = cv.GaussianBlur(frame,(5, 5), 0)
        #blur_frame = cv.medianBlur(frame,3)
        #fgBlurMask = cv.fastNlMeansDenoising(backSub.apply(blur_frame),h=20)
        fgBlurMask = backSub.apply(blur_frame)

        #cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
        #cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
        #           cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))

        #cv.imshow('Frame', frame)
        #cv.imshow('FG Mask', fgMask)
        #cv.imshow('Blur Frame', fgBlurMask)
        img_fg = cv.bitwise_and(frame, frame, mask = fgBlurMask)
        cv.imshow('FG', img_fg)


        keyboard = cv.waitKey(1)
        if keyboard == 'q' or keyboard == 27:
            break

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
    return importer.GetOutput()




fromVid2Mat(args)
