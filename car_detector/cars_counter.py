
import numpy as np
import random as rnd
import cv2
from car_detector.utils import *
from car_detector.make_model import *

class CarDetector:
    def __init__(self, videoClass, video_path) -> None:
        self.videoClass = videoClass
        self.seed = 11
        self.videofile = video_path
        self.cap = cv2.VideoCapture(self.videofile)
        self.model = make_model()
        self.model.load_weights('./car_detector/weights_best.h5')

        self.lower = [0, 0, 0]
        self.upper = [100, 100, 100]

        self.stepSize = 30

        self.lower = np.array(self.lower)
        self.upper = np.array(self.upper)

    def start(self) -> None:
        while(True):

            ret, frame = self.cap.read()
            if(ret == False):
                print('Nothing else to do buddy :c')
                break

            image_masked = self.__process_frame(frame)
            s = 0.25

            #Resize images for computational efficiency
            frame = cv2.resize(frame, None, fx = s ,fy = s)
            image_masked = cv2.resize(image_masked,None, fx = s,fy = s)

            #Run the sliding window detection process
            bbox_list, totalWindows, correct, score = detectionProcess(
                cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),
                self.model, 
                winH=50, 
                winW=50, 
                depth=3, 
                nb_images=1, 
                scale=1, 
                stepSize=self.stepSize, 
                thres_score=0.05
            )

            #Draw the detections
            drawBoxes(frame, bbox_list)

            # Draw detections and road masks
            cv2.imshow('video',sidebyside(frame))
            k = cv2.waitKey(3)

            #QUIT
            if(k & 0xFF == ord('q')):
                cv2.destroyWindow("video")
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def __process_frame(self, frame) -> None:
        #Convert image to HSV from BGR
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Find the pixels that correspond to road
        img_out = cv2.inRange(img_hsv, self.lower, self.upper)

        # Clean from noisy pixels and keep only the largest connected segment
        img_out = post_process(img_out)

        image_masked = frame.copy()

        # Get masked image
        image_masked[img_out == 0] = (0, 0, 0)

        return image_masked
