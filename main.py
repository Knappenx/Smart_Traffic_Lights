
from os import name
from car_detector.main import CarDetector
import logging
from car_detector.states import States
import time

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

class MainApp:
    def __init__(self) -> None:
        self.car_detector_one = CarDetector('./tl_gta1.mp4', './car_detector/cars.xml', States.GREEN_LIGHT.value, 10)
        # self.car_detector_two = CarDetector('./contituyentes_demo.mp4', './car_detector/cars2.xml', States.GREEN_LIGHT.value)
        self.threads = []

    def start(self) -> None:
        self.__start_threads([self.car_detector_one])
        # time.sleep(5)
        # self.car_detector_one.state = States.YELLOW_LIGHT.value

    def __start_threads(self, items: list) -> list:
        logging.info('Starting threads...')
        for item in items:
            item.start()
        
if __name__ == "__main__":
    main_app = MainApp()
    main_app.start()
