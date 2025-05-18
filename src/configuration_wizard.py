"""

"""
from typing import Any
import consts as S
if S.DEV:
    def discover_bulbs():
        time.sleep(1)
        return [{"capabilities": {"id": "0x0000000002dfb19a"}, "ip": "10.10.0.1"},{"capabilities": {"id": "0x0000000002dfb13f"}, "ip": "10.10.0.2"}]
else:
    from yeelight import discover_bulbs
import yaml, os, time
import inquirer as Q
import colorama as CLR
from bulb_wrapper import WrappedBulb


LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

BLUE = lambda i: f"{CLR.Fore.BLUE}{i}{CLR.Style.RESET_ALL}"
 


class Console:
    def __init__(self) -> None:
        self.counter: int = 0
        return 
    
    def print(self, *args, **kwargs) -> None:
        self.counter += 1
        print(*args, **kwargs)

    def refresh(self) -> None:
        if self.counter > 0:
            for _ in range(self.counter):
                print(LINE_UP + LINE_CLEAR, end="")
        self.counter = 0

    def reprint(self, *args, **kwargs) -> None:
        self.refresh()
        self.print(*args, **kwargs)
        return
    

    def input_str(self, *args, **kwargs) -> str:
        self.counter += 1
        return input(*args, **kwargs)
    
    def input_int(self, *args, **kwargs) -> int:
        while True:
            try:
                return int(self.input_str(*args, **kwargs))
            except ValueError as e:
                self.print(f"{CLR.Fore.RED}Invalid input. Please enter an integer.{CLR.Style.RESET_ALL}")
                continue
        

def main() -> None:
    """
    """
    os.system("clear" if os.name == "posix" else "cls")
    print(CLR.Fore.GREEN + S.YEEMIDI_CONFIGURATOR_TEXT + CLR.Style.RESET_ALL)
    con = Console()
    con.print("Querying for Yeelight bulbs...")
    available_bulbs = discover_bulbs()
    con.reprint(f"Found {CLR.Fore.BLUE}{len(available_bulbs)}{CLR.Style.RESET_ALL} bulb(s).")
    time.sleep(3)
    if len(available_bulbs) == 0:
        con.print(f"{CLR.Fore.RED}No bulbs found. Exiting...{CLR.Style.RESET_ALL}")
        return
    export_bulbs: list[WrappedBulb] = list()
    con.refresh()
    for bulb in available_bulbs:
        b = WrappedBulb.from_dict(bulb)
        if b is None:
            continue
        with b.distinguish():
            con.print(f"Setting bulb {BLUE(b.id)} with {BLUE(b.ip)}:")
            con.print(f"This bulb shall have following 'sticker_id':")
            b.sticker_id = con.input_str()
            con.print("This bulb shall be assigned to the following 'group':")
            b.group = int(con.input_int())
            export_bulbs.append(b)
            con.refresh()
    WrappedBulb.to_yaml(export_bulbs, "bulbs.yaml")
    



if __name__ == "__main__":
    main()





