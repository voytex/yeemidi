from yeelight.flow import Flow, Action, TemperatureTransition, RGBTransition, SleepTransition
from typing import List, Optional
import logging
import yaml

import console as CON
import consts as C


logger = logging.getLogger(__name__)


ACTION_TRANSLATION = {"turnoff": Action.off,
                      "recover": Action.recover, "stay": Action.stay}
FUNCTION_TRANSLATION = {"white": TemperatureTransition,
                        "rgb": RGBTransition, "sleep": SleepTransition}
DEFAULT_FLOW: Flow = Flow(1, Action.off, [SleepTransition(50)])
FLOW_TABLE: List[Optional[Flow]] = [None for _ in range(1, 128)]


def initialize_flows(path: str, con: Optional[CON.Console] = None) -> None:
    global FLOW_TABLE
    logger.info(f"Processing flows file {path}")
    if con:
        con.print(f"Reading flows from {C.BLUE(path)}")
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
        for flow_number in data:
            if con:
                con.print(f"Flow number {C.BLUE(flow_number)}: ", end="")
            try:
                count = data[flow_number]["count"]
                action = ACTION_TRANSLATION[data[flow_number]["action"]]
                transitions = []
                for state in data[flow_number]["states"]:
                    #
                    # Shorthand method for retrieving the only key from a dict
                    fx_key = next(iter(state))
                    #
                    # Retrieving the arguments for given transition function
                    args = state[fx_key]
                    transition = FUNCTION_TRANSLATION[fx_key]
                    transitions.append(transition(*args))
                FLOW_TABLE[flow_number] = Flow(count, action, transitions)
                if con:
                    con.print(C.GREEN("Success!"))
            except Exception as e:
                logger.exception(f"Failed to process {flow_number=}")
                if con:
                    con.print(C.RED("Failed!"))
                FLOW_TABLE[flow_number] = DEFAULT_FLOW


def dump_default(path: str) -> None:
    default_yaml = """
# CZ:
# - count = kolikrat se bude retezec 'states' opakovat. '0' -> donekonecna
# - action = co se stane, az retezec skonci. 
#    - 'recover' se vrati do stavu pred spustenim flow
#    - 'stay' zustane v poslednim stavu flow
#    - 'off' vypne zarovku
# - states = jednotlive etapy dane flow. Muzou byt 3:
#   - 'white' nastavi zarovku do bile. 1. argument je teplota, 
#      2. arguent je doba, za kterou se do toho stavuu dostane, 
#      3. argument je konecny jas.
#      Pro priklad: 
#                     - white: [3600, 150, 99] 
#      nastavi tuhle etapu na bilou o teplote 3600 K. Do tehle etapy se bude
#      zarovka nastavovat 150 ms a konecny jas bude 99 %.
#   - 'rgb' nastavi zarovku do RGB. 1. argument je cervena slozka,
#      2. argument je zelena slozka a 3. argument je modra slozka vysledne barvy.
#      Zbyle dva argumenty jsou stejne jako u 'white'.
#      Pro priklad:
#                     - rgb: [255, 0, 255, 300, 20]
#      nastavi tuhle etapu na zhruba fialovou za 300 ms. Vysledny jas bude 20 %.
#   - 'sleep' nenastavuje etapu, ale prodluzuje zacatek te dalsi. Nedeje se nic po 
#     'n' milisekund, kde 'n' je 1. argument. Pozor, i jeden argument zde musi byt 
#      ohranicen hranatyma zavorkama '[]'

1: # strobo
  count: 0
  action: turnoff
  states:
    - white: [3500, 50, 50]
    - sleep: [50]
    - white: [3500, 50, 0]
    - sleep: [50]"""
    with open(path, 'w') as f:
        f.write(default_yaml)


def get_flow(num: int) -> Flow:
    if FLOW_TABLE[num] is not None:
        return FLOW_TABLE[num]
    else:
        logger.error(f"Flow {num=} not present in FLOW_TABLE")
        return DEFAULT_FLOW
