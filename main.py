
from os import name
from car_detector.main import CarDetector
from colorama import Fore, Back, Style
import threading

class TrafficLight:
    def __init__(self) -> None:
        pass
    
    def green(self) -> None:
        print(Fore.GREEN + "Traffic Light is on")

    def red(self) -> None:
        print(Fore.RED + "Traffic Light is off")
    
    def yellow(self) -> None:
        print(Fore.YELLOW + "Traffic Light is flashing")

class MainApp:
    def __init__(self) -> None:
        # self.car_detector_one = CarDetector('./test_video.mp4', './car_detector/cars.xml')
        self.car_detector_two = CarDetector('./contituyentes_demo.mp4', './car_detector/cars2.xml')
        self.traffic_light = TrafficLight()
        # self.__start_threads([self.car_detector_one.start, self.car_detector_two.start])

    def start(self) -> None:
        self.car_detector_two.start()


    ## TODO - Hasta nuevo aviso :v
    def __start_threads(self, items: list) -> list:
        for item in items:
            threading.Thread(target=item).start()
        
if __name__ == "__main__":
    main_app = MainApp()
    main_app.start()