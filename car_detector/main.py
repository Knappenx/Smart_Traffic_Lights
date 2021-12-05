
from time import sleep
import time
import cv2
import logging
from threading import Thread
from car_detector.traffic_light import TrafficLight
from car_detector.states import States
class CarDetector(Thread):
    def __init__(self, video_path, cascade_path, init_state) -> None:
        Thread.__init__(self)
        self.light = TrafficLight()
        self.cascade_path = cascade_path
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.car_cascade = cv2.CascadeClassifier(self.cascade_path)
        self.running = True
        self.state = init_state
        # self.__create_trackbar()


    def __create_trackbar(self):
        cv2.namedWindow("img")
        cv2.createTrackbar('Scale Factor', 'img', 5, 200, self.__parameter_selection)
        cv2.createTrackbar('Min Neighbours', 'img', 10, 100, self.__parameter_selection)

    def run(self):
        self.__green_state()
        while self.running:
            if States.GREEN_LIGHT.value == self.state:
                self.__reproduce()
            if States.YELLOW_LIGHT.value is self.state:
                self.__yellow_state()
            if States.RED_LIGHT.value is self.state:
                self.__red_state(10)
            if States.STOP_APP.value is self.state:
                logging.info("Stopping app...")
                break

        cv2.destroyAllWindows()

    def __reproduce(self) -> None:
        ret, img = self.cap.read()

        if (type(img) == type(None) and ret == False):
            logging.error('No image found')
            exit(1)

        cars = self.__detect_cars(img)
        # print(f'Número de carros contados: {len(cars)}')

        for (x, y, w, h) in cars:
            ## TODO - Lógica para cambiar estado dependiendo de la cantidad de carros detectados y si hay auto de emergencia
            cv2.rectangle(img, (x, y),(x + w, y + h),(0, 0, 255), 2)
            
        cv2.imshow(self.video_path, img)

        if cv2.waitKey(33) == 27:
            self.state = States.STOP_APP.value
    
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

    def __green_state(self):
        self.light.green()
        sleep(1)

    def __red_state(self, seconds):
        self.light.red()
        sleep(seconds)
        self.state = States.GREEN_LIGHT.value

    def __yellow_state(self):
        # start_time = time.clock()
        # seconds = int(time.clock() - start_time)
        self.light.yellow()
        self.state = States.RED_LIGHT.value
