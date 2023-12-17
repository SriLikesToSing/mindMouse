from __future__ import division
import cv2
from .pupil import pupil

class calibrate(object):

    def __init__(self):
        self.frameCount=20
        self.thresholdLeft = []
        self.thresholdRight=[]

    def isComplete(self):
        return len(self.thresholdLeft)>=self.frameCount and len(self.thresholdRight)>=self.frameCount

    def threshold(self, side):    
        if side == 0:
            return int(sum(self.thresholdLeft)/len(self.thresholdLeft))
        elif side ==1:
            return int(sum(self.thresholdRight)/len(self.thresholdRight))
        
    @staticmethod
    def irisSize(frame):
        frame=frame[5:-5, 5:-5]
        height, width=frame.shape[:2]
        pixelCount=height*width
        blackCount=pixelCount-cv2.countNonZero(frame)
        return blackCount/pixelCount

    @staticmethod
    def thresholdFinder(eyeFrame):
        averageIrisSize=0.48
        trials={}

        for threshold in range(5, 100, 5):
            irisFrame=Pupil.imageProcessing(eyeFrame, threshold)
            trials[threshold] = Calibration.irisSize(irisFrame)

        #minimize the differece between average iris size and irisSize for a good threshold value

        #remember, lambda functions go from R^N ---> R^1
        bestThreshold, irisSize = min(trials.items(), key=(lambda p: abs(p[1]-averageIrisSize)))
        return bestThreshold

    def evaluate(self, eyeFrame, side):
        threshold = self.findBestThreshold(eyeFrame)

        if side ==0:
            self.thresholdsLeft.append(threshold)
        elif side==1:
            self.thresholdsRight.append(threshold)


        
