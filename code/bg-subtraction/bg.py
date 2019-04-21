from __future__ import print_function
import cv2 as cv
import argparse
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='/home/mkijowski/videos/VASTChallenge2009-M3-VIDEOPART1.mov')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

if args.algo == 'MOG2':
    #backSub = cv.createBackgroundSubtractorMOG2(detectShadows=0)
    backSub = cv.createBackgroundSubtractorMOG2(history=300,varThreshold=100,detectShadows=1)
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
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    blur_frame = cv.GaussianBlur(frame,(5, 5), 0)
    #blur_frame = cv.medianBlur(frame,3)
    fgBlurMask = cv.fastNlMeansDenoising(backSub.apply(blur_frame),h=20)
    
    #fgMask = backSub.apply(frame)
    #varmax = backSub.getVarMin()
    #print(varmax)

    #cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    #cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
    #           cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))


    #dst = cv.fastNlMeansDenoising(fgMask,None,3,7,11)
    #cv.imshow('FG Mask', dst)
    #cv.imshow('Frame', frame)
    #cv.imshow('FG Mask', fgMask)
    #cv.imshow('Blur Frame', fgBlurMask)
    img_fg = cv.bitwise_and(frame, frame, mask = fgBlurMask)
    cv.imshow('FG', img_fg)
    keyboard = cv.waitKey(1)
    if keyboard == 'q' or keyboard == 27:
        break
