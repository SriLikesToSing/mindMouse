import math 
import numpy as np
import cv2
from .pupil import pupil


class eye(object):
    LEFTEYEPOINTS= [36, 37, 38, 39, 40, 41]
    RIGHTEYEPOINTS= [42, 43, 44, 45, 46, 47]

    def __init__(self, originalFrame, landmarks, side, calibration):
        self.frame = None
        self.origin = None
        self.center = None
        self.pupil = None
        self.landmarkPoints = None
        self.analyze(originalFrame, landmarks, side, calibration)

    @staticmethod
    def middlePoint(point1, point2):
        x = int((point1.x + point2.x)/2)
        y = int((point2.y + point2.y)/2)
        return (x, y)

    def isolateEye(self, frame, landmarks, points):
        region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in points])
        region = region.astype(np.int32)
        self.landmarkPoints = region


        # .shape fetches dimensions of type objects in the form of a tuple
        height, width = frame.shape[:2]
        blackFrame = np.zeros((height, width), np.uint8)
        #what truly is a mask? mathematically.
        # a function from R^n to R^m such that the function is stripped of its parts according to some restriction set {}
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [region], (0, 0, 0))
        eye = cv2.bitwise_not(blackFrame, frame.copy(), mask=mask)

        margin = 5
        minX = np.min(region[:, 0]) - margin
        maxX = np.max(region[:, 0]) + margin
        minY = np.min(region[:, 1]) - margin
        maxY = np.max(region[:, 1]) + margin

        self.frame = eye[minY:maxY, minX:maxX]
        self.origin = (minX, minY)

        height, width = self.frame.shape[:2]
        self.center = (width /2, height/2)

    def blinkingRatio(self, landmarks, points):
        left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y) 
        right= (landmarks.part(points[3]).x, landmarks.part(points[3]).y) 
        #what does .part() do exactly?
        top = self.middlePoint(landmarks.part(points[1]), landmarks.part(points[2]))
        bottom= self.middlePoint(landmarks.part(points[5]), landmarks.part(points[4]))

        eyeWidth=math.hypot((left[0] - right[0]), (left[1] - right[1]))
        eyeHeight=math.hypot((top[0] - bottom[0]), (top[1] - bottom[1]))
        ratio=eyeWidth/eyeHeight

        #such sexy code
        return ratio if ratio != 0 else ValueError("Zero Division Error")

    def analyze(self, originalFrame, landmarks, side, calibration): 
        if side == 0:
            points=self.LEFTEYEPOINTS
        elif side==1:
            points=self.RIGHTEYEPOINTS
        else:
            return
        
        self.blinking = self.blinkingRatio(landmarks, points)
        self.isolateEye(originalFrame, landmarks, points)

        if not calibration.isComplete():
            calibration.evaluate(self.frame, side)
        
        threshold = calibration.threshold(side)
        self.pupil = pupil(self.frame, threshold)

        
























































