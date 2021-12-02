# -*- coding: utf-8 -*-

import cv2
print(cv2.__version__)

class CarDetector:
    def __init__(self, video_path, cascade_path) -> None:
        print("[INFO] loading video...", video_path)
        self.cascade_path = cascade_path
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.car_cascade = cv2.CascadeClassifier(self.cascade_path)
        self.__create_trackbar()

    def __parameter_selection(self, x):
        pass

    def __create_trackbar(self):
        cv2.namedWindow("img")
        cv2.createTrackbar('Scale Factor', 'img', 5, 200, self.__parameter_selection)
        cv2.createTrackbar('Min Neighbours', 'img', 10, 100, self.__parameter_selection)

    def start(self) -> None:
        while True:
            ret, img = self.cap.read()
            if (type(img) == type(None)):
                break
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            scalefactor_track = cv2.getTrackbarPos('Scale Factor', 'img')
            min_neigh_track = cv2.getTrackbarPos('Min Neighbours', 'img')

            if scalefactor_track is 0:
                scalefactor_track = 1
            else:
                cars = self.car_cascade.detectMultiScale(
                    gray, 
                    scaleFactor = (scalefactor_track + 100) / 100, # 1.25 
                    minNeighbors = min_neigh_track, #1
                    minSize=(60, 60), 
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

            print(f'Número de carros contados: {len(cars)}')

            for (x, y, w, h) in cars:
                cv2.rectangle(img, (x, y),(x + w,y + h),(0, 0, 255), 2)      
            
            img.save('frame.jpg')
            cv2.imshow(self.video_path, img)
            
            if cv2.waitKey(33) == 27:
                break

        cv2.destroyAllWindows()
