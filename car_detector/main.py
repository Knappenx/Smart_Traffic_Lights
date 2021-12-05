# -*- coding: utf-8 -*-

from time import sleep
import time
import cv2
import logging
from threading import Thread
from car_detector.traffic_light import TrafficLight
class CarDetector(Thread):
    def __init__(self, video_path, cascade_path, lock) -> None:
        logging.info("Initializing car detector...")
        Thread.__init__(self)
        self.light = TrafficLight()
        self.cascade_path = cascade_path
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.car_cascade = cv2.CascadeClassifier(self.cascade_path)
        self.img = None
        self.lock = lock
        self.running = True
        self.paused = False
        # self.__create_trackbar()


    def __create_trackbar(self):
        cv2.namedWindow("img")
        cv2.createTrackbar('Scale Factor', 'img', 5, 200, self.__parameter_selection)
        cv2.createTrackbar('Min Neighbours', 'img', 10, 100, self.__parameter_selection)

    def run(self):
        logging.info("Starting video...")
        self.__reproduce_video()

    def __reproduce_video(self) -> None:
        # self.lock.acquire()
        start_time = time.clock()
        while self.running:
            # seconds = int(time.clock() - start_time)
            # print('Seconds: ', seconds)
            ret, self.img = self.cap.read()
            if (type(self.img) == type(None) and ret == False):
                break
            cars = self.__detect_cars(self.img)
            # print(f'Número de carros contados: {len(cars)}')
            for (x, y, w, h) in cars:
                cv2.rectangle(self.img, (x, y),(x + w, y + h),(0, 0, 255), 2)
                
            cv2.imshow(self.video_path, self.img)

            if self.paused is True:
                cv2.imshow(self.video_path, self.img)
                self.light.green()
                time.sleep(self.seconds)
                self.paused = False

            if cv2.waitKey(33) == 27:
                break

        cv2.destroyAllWindows()
    
    def __detect_cars(self, img) -> list:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        scalefactor_track = cv2.getTrackbarPos('Scale Factor', 'img')
        min_neigh_track = cv2.getTrackbarPos('Min Neighbours', 'img')

        if scalefactor_track is 0:
            scalefactor_track = 1
        else:
            cars = self.car_cascade.detectMultiScale(
                gray, 
                scaleFactor = (125 + 100) / 100, # 1.25 
                minNeighbors = 1, #1
                minSize=(60, 60), 
                flags=cv2.CASCADE_SCALE_IMAGE
            )

        return cars

    def pause(self, seconds):
        logging.info("Pausing video...")
        self.seconds = seconds
        self.paused = True

    def resume(self):
        pass

    def stop(self):
        logging.info("Stopping video...")
        self.running = False
        # self.cap.release()
        # cv2.destroyAllWindows()