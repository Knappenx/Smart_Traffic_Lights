import logging
from colorama import Fore, Back, Style

class TrafficLight:        
    
    def green(self) -> None:
        logging.info(Fore.GREEN + "Traffic Light is on")
        Style.RESET_ALL

    def red(self) -> None:
        logging.info(Fore.RED + "Traffic Light is off")
        Style.RESET_ALL
    
    def yellow(self) -> None:
        logging.info(Fore.YELLOW + "Traffic Light is flashing")
        Style.RESET_ALL