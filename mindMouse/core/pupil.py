import numpy as np
import cv2


class pupil(object):
    def __init__(self, eyeFrame, threshold):
        self.irisFrame=None
        self.threshold=threshold
        self.x=None
        self.y=None
        self.detectIris(eyeFrame)

    @staticmethod
    def isolateIris(eyeFrame, threshold):
        kernel=np.ones((3,3), np.uint8)
        newFrame=cv2.bilateralFilter(eyeFrame,10,15,15)
        newFrame=cv2.erode(newFrame, kernel,iterations=3)
        newFrame=cv2.threshold(newFrame,threshold,255,cv2.THRESH_BINARY)[1]

        return newFrame

    def detectIris(self, eyeFrame):
        self.irisFrame=self.isolateIris(eyeFrame,self.threshold)

        contours,_=cv2.findContours(self.irisFrame,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        contours=sorted(contours, key=cv2.contourArea)

        try:
            moments = cv2.moments(contours[-2])
            self.x=int(moments['m10']/moments['m00'])
            self.y=int(moments['m01']/moments['m00'])
        except(IndexError, ZeroDivisionError):
            pass


































