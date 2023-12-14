import math 
import numpy as np
import cv2


class eye(object):
    LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
    RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]

    def __init__(self, original_frame, landmarks, side, calibration):
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

        height, width = frame.shape[:2]
        blackFrame = np.zeros((height, width), np.uint8)
        #what truly is a mask? mathematically.
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





















































