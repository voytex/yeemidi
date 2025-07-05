from typing import List, Tuple
from rtmidi2 import MidiIn, splitchannel, NOTEON, NOTEOFF
import argparse
import threading
import logging
import os
import sys

from thread_prototype import ThreadInterface, group_thread
import midi_bulb as MB
import proto as P
import consts as C
import console as CON
import version as V

logger = logging.getLogger()

TI = [ThreadInterface(
    new_data=False,
    lock=False,
    cmd="rgb",
    rgb=[0, 0, 0],
    white_temp=2700,
    brightness=0,
    pwr=False,
    to_off=False,
    time=30,
    chase_number=0,
    terminate=False
) for _ in range(1, C.GROUP_COUNT + 1)]


def midi_callback(msg: List[int], timestamp: float) -> None:
    type, channel = splitchannel(msg[0])
    channel += 1
    logger.debug(
        f"Received MIDI message: {type=} on {channel=} at {timestamp}")
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
    #
    # Logger setup
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s", filename="yeemidi.log")
    #
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Yeelight Main")
    parser.add_argument(
        "-f", "--file", help="Configuration file, exported by 'wizard_configuration.py'", default="config.yml")
    args = parser.parse_args()
    #
    # UI setup
    os.system("clear" if os.name == "posix" else "cls")
    print(C.GREEN(C.YEEMIDI_MAIN_TEXT))
    print(f"Version: {C.GREEN(V.VERSION)}")
    if not os.path.isfile(args.file):
        print(C.RED(
            f"File '{args.file}' not found.\nCreate it using 'wizard_configuration.py'."))
        sys.exit(1)
    con = CON.Console()
    #
    # Initiation
    con.print(f"Starting using {C.BLUE(args.file)} configuration file")
    midi_in = MidiIn()
    midi_in.open_virtual_port("yeemidi")
    midi_in.callback = midi_callback
    try:
        grouped_bulbs = MB.from_yaml(args.file)
    except ValueError as e:
        con.print(C.RED(
            f"Not all bulbs from config file {args.file} are available on the network"))
        logger.error(
            f"Bulbs from config file {args.file} are not available on the network: {e}")
        sys.exit(1)
    group_threads_list: List[threading.Thread] = []
    #
    # Launching threads
    for group, bulbs_in_group in grouped_bulbs.items():
        group_threads_list.append(
            threading.Thread(target=group_thread,
                             args=(bulbs_in_group, TI[group]))
        )
    for thread in group_threads_list:
        thread.start()
    con.reprint(f"{C.GREEN('Running!')} Type 'x' and 'Enter' to terminate.")
    #
    # Main waiting loop
    try:
        while True:
            key = con.input_str()
            if key.lower() == 'x':
                con.reprint(C.RED("Terminating."))
                for ti in TI:
                    ti.terminate = True
                break
    except KeyboardInterrupt:
        con.reprint(C.RED("Terminating."))
        for ti in TI:
            ti.terminate = True
    for thread in group_threads_list:
        thread.join()
    midi_in.close_port()


if __name__ == "__main__":
    main()
