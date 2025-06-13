
from dataclasses import dataclass
from typing import List, Literal, Tuple
from midi_bulb import MidiBulb, MidiBulbCollection


@dataclass
class ThreadInterface:
    new_data: bool
    lock: bool
    cmd: Literal["rgb", "white", "brightness",  "pwr"]
    rgb: Tuple[int, int, int]
    white_temp: int
    brightness: int
    pwr: bool
    time: int


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
                bulb.set_rgb(*ti.rgb, duration=ti.time)
            elif ti.cmd == "white":
                bulb.set_color_temp(ti.white_temp, duration=ti.time)
            elif ti.cmd == "brightness":
                bulb.set_brightness(ti.brightness, duration=ti.time)
            elif ti.cmd == "pwr":
                [bulb.turn_off, bulb.turn_on][ti.pwr](duration=ti.time)
        ti.lock = False
        ti.new_data = False