from __future__ import division
import os 
import cv2
import dlib
from .eye import eye
from .calibrate import calibrate 

class eyeTracker(object):
   
    def __init__(self):
        self.frame = None
        self.rightEye = None
        self.leftEye = None
        self.calibration = calibrate()
        self.faceDetector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("./core/shape_predictor_68_face_landmarks.dat")


    @property 
    def pupilsDetected(self): 
        try:
            int(self.leftEye.pupil.x)
            int(self.leftEye.pupil.y)
            int(self.rightEye.pupil.x)
            int(self.rightEye.pupil.y)
            return True
        except Exception:
            return False

    def analyze(self):
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceDetector(frame)

        try:
            landmarks = self.predictor(frame, faces[0])
            self.rightEye = eye(frame, landmarks, 0, self.calibration)
            self.leftEye = eye(frame, landmarks, 1, self.calibration)
        except IndexError:
            self.leftEye = None
            self.rightEye = None

    def refresh(self, frame):
        self.frame = frame
        self.analyze() 

    def leftEyeCordinates(self):
        if self.pupilsDetected:
            x = self.leftEye.origin[0] + self.leftEye.pupil.x
            y = self.leftEye.origin[1] + self.leftEye.pupil.y
            return (x, y)

    def rightEyeCordinates(self):
        if self.pupilsDetected:
            x = self.rightEye.origin[0] + self.rightEye.pupil.x
            y = self.rightEye.origin[1] + self.rightEye.pupil.y
            return (x, y)
    
    def horitontalEyeDirection(self):
        if self.pupilsDetected:
            leftEye = self.leftEye.pupil.x / (self.leftEye.center[0] * 2 -10)
            rightEye = self.rightEye.pupil.x / (self.rightEye.center[0] * 2 -10)
            return (leftPupil + rightPupil)/2

    def verticalEyeDirection(self):
        if self.pupilsDetected:
            leftEye = self.leftEye.pupil.y / (self.leftEye.center[1] * 2 -10)
            rightEye = self.rightEye.pupil.y / (self.rightEye.center[1] * 2 -10)
            return (leftPupil + rightPupil)/2

    def lookingRight(self):
        if self.pupilsDetected:
            return self.horizontalEyeDirection() <= 0.35

    def lookingLeft(self):
        if self.pupilsDetected:
            return self.horizontalEyeDirection() <= 0.65

    def lookingCenter(self):
        if self.pupilsDetected:
            return self.lookingLeft is not True and lookingRight is not True

    def isBlinking(self):
        if self.pupilsDetected:
            blinkingRatio = (self.leftEye.blinking + self.rightEye.blinking)/2
            return blinkingRatio > 3.8

    def frameData(self):
        frame = self.frame.copy()

        if self.pupilsDetected:
            color = (0, 255, 0)
            xLeft, yLeft = self.leftEyeCordinates()
            xRight, yRight = self.rightEyeCordinates()
            cv2.line(frame, (xLeft - 5, yLeft), (xLeft+5, yLeft), color)
            cv2.line(frame, (xLeft, yLeft -5), (xLeft, yLeft +5), color)
            cv2.line(frame, (xRight-5, yRight), (xRight+5, yRight), color)
            cv2.line(frame, (xRight, yRight-5), (xRight, yRight+5), color)
        return frame














        



























