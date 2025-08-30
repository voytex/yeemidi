import logging
import os
import argparse
import console as CON
import consts as C
import midi_bulb as MB

logger = logging.getLogger(__name__)


def main() -> None:
    #
    # Arguments parsing
    parser = argparse.ArgumentParser(description="Yeelight lightcheck")
    parser.add_argument("-f", "--file", type=str,
                        help="File to load configuration from.", default="config.yml")
    args = parser.parse_args()
    #
    # Logging initiation
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s", filename="lightcheck.log")
    logger.info("Yeelight lightcheck started.")
    #
    # Console initiation
    os.system("clear" if os.name == "posix" else "cls")
    print(C.GREEN(C.YEEMIDI_LIGHTCHECK_TEXT))
    con = CON.Console()
    greouped_bulbs = MB.from_yaml(args.file)
    for channel, bulbs_in_channel in greouped_bulbs.items():
        con.print(f"Checking channel {C.BLUE(channel)}:")
        con.print(
            f"Found {C.BLUE(len(bulbs_in_channel))} bulb(s) in this channel.")
        with MB.distinguish_channel(bulbs_in_channel):
            con.input_str("Press Enter to continue...")
        con.refresh()


if __name__ == "__main__":
    main()
