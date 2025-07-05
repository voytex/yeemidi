from typing import List, Tuple
from rtmidi2 import MidiIn, splitchannel, NOTEON, NOTEOFF
import argparse
import threading
import logging

from thread_prototype import ThreadInterface, group_thread
import midi_bulb as MB
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
    to_off=False,
    time=30,
    chase_number=0
) for _ in range(1, C.GROUP_COUNT + 1)]


def midi_callback(msg: List[int], timestamp: float) -> None:
    type, channel = splitchannel(msg[0])
    channel += 1  
    logger.debug(f"Received MIDI message: {type=} on {channel=} at {timestamp}")
    if type != NOTEON:
        return
    note_num = msg[1]
    velocity = msg[2]
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
    elif note_num == P.TO_OFF:
        TI[channel].set_to_off(velocity)
    elif note_num == P.TURN_OFF:
        TI[channel].turn_off(velocity)
    elif note_num == P.GO:
        TI[channel].go(velocity) 
    elif note_num == P.CHASE:
        TI[channel].set_chase_number(velocity)


def main() -> None:
    # argparse business
    logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s", filename="yeemidi.log")
    midi_in = MidiIn()
    midi_in.open_virtual_port("yeemidi")
    midi_in.callback = midi_callback
    grouped_bulbs = MB.from_yaml()
    group_threads_list: List[threading.Thread] = []
    for group, bulbs_in_group in grouped_bulbs.items():
        group_threads_list.append(
            threading.Thread(target=group_thread, args=(bulbs_in_group, TI[group]))
        )
        
    for thread in group_threads_list:
        thread.start()

    while True:
        pass


if __name__ == "__main__":
    main() 