
from dataclasses import dataclass
from typing import Callable, List, Literal, Tuple
from midi_bulb import MidiBulb, MidiBulbCollection
import logging


logger = logging.getLogger(__name__)


def check_lock(fn):
    def wrapper(self, *args, **kwargs):
        logger.debug(f"Calling {fn.__name__} with args: {args}, kwargs: {kwargs}")
        if self.lock:
            logger.error(f"Tried to edit locked interface: {fn.__name__=}")
            return
        return fn(self, *args, **kwargs)
    return wrapper

@dataclass
class ThreadInterface:
    new_data: bool
    lock: bool
    cmd: Literal["rgb", "white", "brightness",  "pwr"]
    rgb: List[int]
    white_temp: int
    brightness: int
    pwr: bool
    time: int


    @check_lock
    def go(self, duration: int) -> None:
        self.time = duration
        self.new_data = True


    @check_lock
    def set_white(self, temp: int) -> None:
        self.cmd = "white"
        self.white_temp = temp


    @check_lock
    def set_brightness(self, b: int) -> None:
        self.cmd = "brightness"
        self.brightness = b


    @check_lock
    def set_red(self, r: int) -> None:
        self.cmd = "rgb"
        self.rgb[0] = r

    
    @check_lock
    def set_green(self, g: int) -> None:
        self.cmd = "rgb"
        self.rgb[1] = g
    
    
    @check_lock
    def set_blue(self, b: int) -> None:
        self.cmd = "rgb"
        self.rgb[2] = b


def group_thread(bc: List[MidiBulb], ti: ThreadInterface):
    """
    TODO: 
    """
    for bulb in bc:
#        bulb.stop_music()
        bulb.start_music()
    while True:
        if not ti.new_data:
            continue
        # new data received
        ti.lock = True
        for bulb in bc:
            if ti.cmd == "rgb":
                bulb.set_rgb(ti.rgb[0], ti.rgb[1], ti.rgb[2], duration=ti.time)
            elif ti.cmd == "white":
                bulb.set_color_temp(ti.white_temp, duration=ti.time)
            elif ti.cmd == "brightness":
                bulb.set_brightness(ti.brightness, duration=ti.time)
            elif ti.cmd == "pwr":
                if ti.pwr:
                    bulb.turn_on(duration=ti.time)
                else:
                    bulb.turn_off(duration=ti.time)
        ti.lock = False
        ti.new_data = False