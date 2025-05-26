"""

"""
import os, time, logging, argparse
from typing import List
import consts as C
import console as CON
if C.DEV:
    def discover_bulbs():
        time.sleep(1)
        return [{"capabilities": {"id": "0x0000000002dfb19a"}, "ip": "10.10.0.1"},{"capabilities": {"id": "0x0000000002dfb13f"}, "ip": "10.10.0.2"}]
else:
    from yeelight import discover_bulbs
import colorama as CLR
from midi_bulb import MidiBulb


logger = logging.getLogger()


        

def main() -> None:
    """
    """
    #
    # Arguments parging
    parser = argparse.ArgumentParser(description="Yeelight configurator")
    parser.add_argument("-f", "--file", type=str, help="File to export configuration to.", default="config.yml")
    args = parser.parse_args()
    #
    # Logging initiation
    logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s", filename="ye_conf.log")
    logger.info("Yeelight configurator started.")
    # 
    # Console initiation
    os.system("clear" if os.name == "posix" else "cls")
    print(C.GREEN(C.YEEMIDI_CONFIGURATOR_TEXT))
    con = CON.Console() 
    #
    # Bulbs discovery
    con.print("Querying for Yeelight bulbs...")
    available_bulbs = discover_bulbs()
    con.reprint(f"Found {CLR.Fore.BLUE}{len(available_bulbs)}{CLR.Style.RESET_ALL} bulb(s).")
    time.sleep(3)
    if len(available_bulbs) == 0:
        con.print(f"{CLR.Fore.RED}No bulbs found. Exiting...{CLR.Style.RESET_ALL}")
        return
    export_bulbs: List[MidiBulb] = list()
    con.refresh()
    for bulb in available_bulbs:
        b = MidiBulb(bulb)
        if b is None:
            continue
        with b.distinguish():
            con.print(f"Setting bulb {C.BLUE(b.id)} with {C.BLUE(b.ip)}:")
            con.print(f"This bulb shall have following 'sticker_id':")
            b.sticker_id = con.input_str()
            con.print("This bulb shall be assigned to the following 'group':")
            b.group = int(con.input_int())
            export_bulbs.append(b)
            con.refresh()
    MidiBulb.to_yaml(export_bulbs, args.file)
    con.print(C.GREEN(f"Configuration exported to {C.BLUE(args.file)}."))
    

if __name__ == "__main__":
    main()





