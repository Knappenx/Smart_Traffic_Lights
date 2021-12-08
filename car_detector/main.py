
from time import sleep
import time
import schedule
import cv2
import logging
from threading import Thread
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from car_detector.traffic_light import TrafficLight
from car_detector.states import States

class CarDetector(Thread):
    def __init__(self, video_path, cascade_path, init_state, time_sleep) -> None:
        Thread.__init__(self)
        self.light = TrafficLight()
        self.cascade_path = cascade_path
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.car_cascade = cv2.CascadeClassifier(self.cascade_path)
        self.running = True
        self.state = init_state
        self.model = load_model('./car_detector/firet_recog.h5')
        self.time_sleep = time_sleep
        # self.__create_trackbar()

    def __parameter_selection(self, x):
        pass

    def __create_trackbar(self):
        cv2.namedWindow("img")
        cv2.createTrackbar('Scale Factor', 'img', 5, 200, self.__parameter_selection)
        cv2.createTrackbar('Min Neighbours', 'img', 10, 100, self.__parameter_selection)

    def run(self):
        self.__green_state()
        while self.running:
            self.__state_machine()
            schedule.run_pending()
            time.sleep(1)

        cv2.destroyAllWindows()

    def __state_machine(self):
        if States.GREEN_LIGHT.value is self.state:
            self.__reproduce()
        if States.YELLOW_LIGHT.value is self.state:
            self.__yellow_state()
        if States.RED_LIGHT.value is self.state:
            self.__red_state()
        if States.STOP_APP.value is self.state:
            logging.info("Stopping app...")
            exit(1)

    def __reproduce(self):
        schedule.every(self.time_sleep).seconds.do(self.__validate_state)
        cars_list=[]
        preds=[]
        ret, frame = self.cap.read()

        if (type(frame) == type(None) and ret == False):
            logging.error('No image found')
            exit(1)
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cars = self.car_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 3,
            minSize = (60, 60),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in cars:
            car_frame = self.__detect_car(cars_list, frame, x, y, w, h)
            cars_list.append(car_frame)

            if len(cars_list) > 0:
                preds = self.model.predict(cars_list)

            for pred in preds:
                (car, emergency_car) = pred
            
            label = "Carro de emergencia"
            color = (0, 0, 255)
            if car > emergency_car:
                label = "Carro"
                color = (0, 255, 0)

            label = "{}: {:.2f}%".format(label, max(car, emergency_car) * 100)
            cv2.putText(frame, label, (x, y- 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h),color, 2)

            cv2.imshow('Video', frame)
            k = cv2.waitKey(1)
            if k == 27 or k ==ord('q'):
                exit(1)
                # break
    
    def __detect_car(self, cars: list, frame, x, y, w, h) -> list:
        car_frame = frame[y:y+h,x:x+w]
        car_frame = cv2.resize(car_frame, (224, 224))
        car_frame = cv2.cvtColor(car_frame, cv2.COLOR_BGR2RGB)        
        car_frame = img_to_array(car_frame)
        car_frame = np.expand_dims(car_frame, axis=0)
        car_frame =  preprocess_input(car_frame)

        return car_frame       

    def __validate_state(self):
        print("Validating state...", self.state == States.GREEN_LIGHT.value)
        if self.state == States.GREEN_LIGHT.value:
           self.__red_state()
        if self.state == States.RED_LIGHT.value:
            self.__green_state()

    def __green_state(self):
        self.light.green()
        sleep(5)
        self.state = States.RED_LIGHT.value
        # sleep(10)

    def __red_state(self):
        self.light.red()
        sleep(5)
        self.state = States.GREEN_LIGHT.value

    def __yellow_state(self):
        # start_time = time.clock()
        # seconds = int(time.clock() - start_time)
        self.light.yellow()
        self.state = States.RED_LIGHT.value
