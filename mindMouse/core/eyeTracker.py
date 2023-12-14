from __future__ import division
import os 
import cv2
import dlib

class EyeTracker(FRAME):
   
    def __init__(self):
        self.frame = None
        self.rightEye = None
        self.leftEye = None
        #self.calibration = Calibration()
        self.faceDetector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


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









        



























