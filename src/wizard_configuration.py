import os
import time
import logging
import argparse
from typing import Dict, List
import consts as C
import console as CON
import midi_bulb as MB
import colorama as CLR


logger = logging.getLogger()


def main() -> None:
    """
    """
    #
    # Arguments parging
    parser = argparse.ArgumentParser(description="Yeelight configurator")
    parser.add_argument("-f", "--file", type=str,
                        help="File to export configuration to.", default="config.yml")
    args = parser.parse_args()
    #
    # Logging initiation
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s", filename="configuration.log")
    logger.info("Yeelight configurator started.")
    #
    # Console initiation
    os.system("clear" if os.name == "posix" else "cls")
    print(C.GREEN(C.YEEMIDI_CONFIGURATOR_TEXT))
    con = CON.Console()
    #
    # Bulbs discovery
    con.print("Querying for Yeelight bulbs...")
    available_bulbs = MB.MidiBulb.discover()
    con.reprint(f"Found {C.BLUE(len(available_bulbs))} bulb(s).")
    time.sleep(3)
    if len(available_bulbs) == 0:
        con.print(C.RED("No bulbs found. Exiting..."))
        return
    available_bulbs = MB.MidiBulb.discover()
    grouped_bulbs: Dict[int, List[MB.MidiBulb]] = {}
    con.refresh()
    for b in available_bulbs:
        if b is None:
            continue
        with b.distinguish():
            con.print(f"Setting bulb {C.BLUE(b.id)}:")
            con.print(f"This bulb shall have following 'sticker_id':")
            b.sticker_id = con.input_str()
            con.print("This bulb shall be assigned to the following 'group':")
            b.group = int(con.input_int())
            if b.group not in grouped_bulbs.keys():
                grouped_bulbs[b.group] = []
            grouped_bulbs[b.group].append(b)
            logger.info(
                f"Bulb {b.id} with sticker ID {b.sticker_id} assigned to group {b.group}.")
            con.refresh()
    MB.to_yaml(grouped_bulbs, args.file)
    con.print(C.GREEN(f"Configuration exported to {C.BLUE(args.file)}."))


if __name__ == "__main__":
    main()
