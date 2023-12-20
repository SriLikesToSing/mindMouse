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

def moveMouse(eyeTracker, right, left, up, down):
    # if true, false pair, then 



while True:
    ret, frame = cap.read()
    iTracker.refresh(frame)

    frame = iTracker.frameData()
    text=""

    pos = mouse.get_position()

#    print("Horizontal Direction " , iTracker.horizontalEyeDirection(), ":", " Vertical Direction ", iTracker.verticalEyeDirection())

    if iTracker.isBlinkingRight():
        mouse.click('right')

    if iTracker.isBlinkingLeft():
        mouse.click('left')

    if iTracker.lookingRight():
        mouse.move(pos[0]+1, pos[1], duration=0)
        text="looking right"

    if iTracker.lookingLeft():
        mouse.move(pos[0]-1, pos[1], duration=0)    
        text="looking left"

    if iTracker.lookingUp():
        mouse.move(pos[0], pos[1]-1, duration=0)

    if iTracker.lookingDown():
        mouse.move(pos[0], pos[1]+1, duration=0)
        
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
























