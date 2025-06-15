from typing import List, Tuple
from rtmidi2 import MidiIn, splitchannel, NOTEON, NOTEOFF
import argparse
import threading
import logging

from thread_prototype import ThreadInterface, group_thread
from midi_bulb import MidiBulb
import proto as P
import consts as C


logger = logging.getLogger()

TI = [ThreadInterface(
    new_data=False,
    lock=False,
    cmd="rgb",
    rgb=[0,0,0],
    white_temp=2700,
    brightness=0,
    pwr=False,
    time=30
) for _ in range(C.GROUP_COUNT)]


def midi_callback(msg: List[int], timestamp: float) -> None:
    type, channel = splitchannel(msg[0])
    if type != NOTEON:
        return
    note_num = msg[1]
    velocity = msg[2]
    print(channel, note_num, velocity)
    if note_num == P.BLUE:
        TI[channel].set_blue(velocity)
    elif note_num == P.GREEN:
        TI[channel].set_green(velocity)
    elif note_num == P.RED:
        TI[channel].set_red(velocity)
    elif note_num == P.WHITE:
        TI[channel].set_white(velocity)
    elif note_num == P.BRIGHTNESS:
        TI[channel].set_brightness(velocity)
    elif note_num == P.GO:
        TI[channel].go(velocity) 


def main() -> None:
    # argparse business
    logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s", filename="yeemidi.log")
    midi_in = MidiIn()
    midi_in.open_virtual_port("yeemidi")
    midi_in.callback = midi_callback
    b1 = MidiBulb("0x000000001e5486ae")
    t1 = threading.Thread(target=group_thread, args=([b1], TI[0]))
    b1.turn_on()
    t1.start()
    while True:
        pass


if __name__ == "__main__":
    main() 