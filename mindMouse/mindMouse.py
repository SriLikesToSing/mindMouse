import cv2
import random
import numpy as np
from core import eyeTracker 
import mouse

cap = cv2.VideoCapture(0)
iTracker=eyeTracker()

if not cap.isOpened():
    print('hello')
    raise IOError("Cannot open webcam")



while True:
    ret, frame = cap.read()
    iTracker.refresh(frame)

    frame = iTracker.frameData()
    text=""

    if iTracker.isBlinking():
        text="currently blinking"
    elif iTracker.lookingRight():
        text="looking right"
    elif iTracker.lookingLeft():
        text="looking left"
    elif iTracker.lookingCenter():
        text="looking center"
    elif iTracker.isBlinkingLeft():
        text="right click engaged"
        mouse.click('right')
    elif iTracker.isBlinkingRight():
        text="left click engaged"
        mouse.click('left')





    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    leftPupil = iTracker.leftEyeCordinates()
    rightPupil = iTracker.rightEyeCordinates()
    cv2.putText(frame, "Left pupil: " + str(leftPupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil" + str(rightPupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


    cv2.imshow('application', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break


cap.release()
cv2.destroyAllWindows()
























