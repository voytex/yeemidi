"""

"""

import logging, os, argparse
import console as CON
import consts as C
import midi_bulb as MB

logger = logging.getLogger(__name__)


def main() -> None:
    #
    # Arguments parsing
    parser = argparse.ArgumentParser(description="Yeelight lightcheck")
    parser.add_argument("-f", "--file", type=str, help="File to load configuration from.", default="config.yml")
    args = parser.parse_args()
    #
    # Logging initiation
    logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s", filename="ye_conf.log")
    logger.info("Yeelight lightcehck started.")
    #
    # Console initiation
    os.system("clear" if os.name == "posix" else "cls")
    print(C.GREEN(C.YEEMIDI_LIGHTCHECK_TEXT))
    con = CON.Console()
    greouped_bulbs = MB.from_yaml(args.file)
    for group, bulbs_in_group in greouped_bulbs.items():
        con.print(f"Checking group {C.BLUE(group)}:")
        con.print(f"Found {C.BLUE(len(bulbs_in_group))} bulb(s) in this group.")
        with MB.distinguish_group(bulbs_in_group):
            con.input_str("Press Enter to continue...")
        con.refresh()

        
            
            


if __name__ == "__main__":
    main()