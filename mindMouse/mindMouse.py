import cv2
import random
import numpy as np
from core import eyeTracker 
import mouse

cap = cv2.VideoCapture('http://192.168.0.5:8080/video')
iTracker=eyeTracker()

if not cap.isOpened():
    print('hello')
    raise IOError("Cannot open webcam")

def moveMouse(pos, right, left, up, down):
    # if true, false pair, then dirhor=+1 else -1
    # if true, false pair, then dirver=+1 else -1

    dirhor= 1 if right and not left else -1 if not right and left else 0
    dirver= 1 if up and not down else -1 if not up and down else 0
    print("DIRHORIZONTAL : " , dirhor)

    mouse.move(pos[0]+dirhor*4, pos[1]+dirver*4, duration=0)

while True:
    ret, frame = cap.read()
    iTracker.refresh(frame)

    frame = iTracker.frameData()
    text=""

    pos = mouse.get_position()

    moveMouse(pos, iTracker.lookingRight(), iTracker.lookingLeft(), iTracker.lookingUp(), iTracker.lookingDown())

    if iTracker.isBlinkingRight():
        mouse.click('right')

    if iTracker.isBlinkingLeft():
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
























