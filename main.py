
from os import name
from car_detector.main import CarDetector
import threading
lock = threading.Lock()
import logging
import cv2
import time
logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

class MainApp:
    def __init__(self) -> None:
        self.car_detector_one = CarDetector('./test_video.mp4', './car_detector/cars.xml', lock)
        self.car_detector_two = CarDetector('./contituyentes_demo.mp4', './car_detector/cars2.xml', lock)
        self.threads = []

    def start(self) -> None:
        self.__start_threads([self.car_detector_one, self.car_detector_two])
        time.sleep(5)
        self.car_detector_one.pause(10)

    def __start_threads(self, items: list) -> list:
        logging.info('Starting threads...')
        for i, item in enumerate(items):
            item.start()
            print(item)
        
if __name__ == "__main__":
    main_app = MainApp()
    main_app.start()
