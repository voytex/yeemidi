
from dataclasses import dataclass
from typing import List, Literal, Tuple
import midi_bulb as MB
import logging
import yeelight as Y
import yeelight.flow as YF

from flows_table import get_flow

COLOR_TEMP_MULTIPLIER = 37.79527
COLOR_TEMP_OFFSET = 1700
def MIDI_CC_TO_PERCENT(x): return int((x / 127.0) * 100.0)


MIN_MS = 30
MAX_MS = 10000
def MIDI_CC_TO_MS(x): return int((x * ((MAX_MS - MIN_MS) / 127)) + MIN_MS)


logger = logging.getLogger(__name__)


def check_lock(fn):
    def wrapper(self, *args, **kwargs):
        logger.debug(
            f"Calling {fn.__name__} with args: {args}, kwargs: {kwargs}")
        if self.lock:
            logger.error(f"Tried to edit locked interface: {fn.__name__=}")
            return
        return fn(self, *args, **kwargs)
    return wrapper


@dataclass
class ThreadInterface:
    new_data: bool
    lock: bool
    cmd: Literal["rgb", "white",  "off", "chase"]
    rgb: List[int]
    time: int
    white_temp: int
    brightness: int
    chase_number: int
    to_off: bool
    pwr: bool
    terminate: bool

    @check_lock
    def turn_off(self, duration: int) -> None:
        self.time = MIDI_CC_TO_MS(duration)
        self.cmd = "off"
        self.new_data = True

    @check_lock
    def go(self, duration: int) -> None:
        """
        :param duration: Duration in MIDI CC range (0-127).
        """
        self.time = MIDI_CC_TO_MS(duration)
        self.new_data = True

    @check_lock
    def set_to_off(self, value) -> None:
        if value > 64:
            self.to_off = True
        else:
            self.to_off = False

    @check_lock
    def set_white(self, temp: int) -> None:
        """
        :param temo: Color temperature in MIDI CC range (0-127).
        """
        self.cmd = "white"
        self.white_temp = int(COLOR_TEMP_OFFSET +
                              (temp * COLOR_TEMP_MULTIPLIER))

    @check_lock
    def set_red(self, r: int) -> None:
        """
        :param r: Red component in MIDI CC range (0-127).
        """
        self.cmd = "rgb"
        self.rgb[0] = MIDI_CC_TO_PERCENT(r)

    @check_lock
    def set_green(self, g: int) -> None:
        """
        :param g: Green component in MIDI CC range (0-127).
        """
        self.cmd = "rgb"
        self.rgb[1] = MIDI_CC_TO_PERCENT(g)

    @check_lock
    def set_chase_number(self, num: int) -> None:
        self.cmd = "chase"
        self.chase_number = num

    @check_lock
    def set_blue(self, b: int) -> None:
        """
        :param b: Blue component in MIDI CC range (0-127).
        """
        self.cmd = "rgb"
        self.rgb[2] = MIDI_CC_TO_PERCENT(b)

    @check_lock
    def set_brightness(self, brightness: int) -> None:
        self.brightness = MIDI_CC_TO_PERCENT(brightness)

    def stop(self):
        self.terminate = True


def channel_thread(bc: List[MB.MidiBulb], ti: ThreadInterface):
    """
    TODO: 
    """
    logger.info("Starting channel thread with following bulbs: " +
                ", ".join([bulb.id for bulb in bc]))
    for bulb in bc:
        bulb.start_music()
        bulb.turn_on()
    while not ti.terminate:
        if not ti.new_data:
            continue
        # new data received
        logger.debug(f"Thread Locked and Sending ")
        ti.lock = True
        action = YF.Action.off if ti.to_off else YF.Action.stay
        for bulb in bc:
            try:
                if ti.cmd == "rgb":
                    flow = Y.Flow(1, action, [Y.RGBTransition(
                        *ti.rgb, brightness=ti.brightness, duration=ti.time)])
                    bulb.set_scene(Y.SceneClass.CF, flow)
                elif ti.cmd == "white":
                    flow = Y.Flow(1, action, [Y.TemperatureTransition(
                        ti.white_temp, duration=ti.time, brightness=ti.brightness)])
                    bulb.set_scene(Y.SceneClass.CF, flow)
                elif ti.cmd == "chase":
                    bulb.set_scene(Y.SceneClass.CF, get_flow(ti.chase_number))
                elif ti.cmd == "off":
                    bulb.turn_off(duration=ti.time)
            except Exception as e:
                logger.error(f"Failed to send command to bulb {bulb.id}:\n{str(e)}\nTrying to reconnect...")
                #
                # This will try to establish new connection using new sockets.
                bulb.start_music()
        ti.lock = False
        ti.new_data = False
    for bulb in bc:
        try:
            bulb.stop_music()
        except Y.BulbException as e:
            logger.error(f"Failed to stop music on bulb {bulb.id}: {e}")
