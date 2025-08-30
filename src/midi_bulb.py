"""

"""
from contextlib import contextmanager, suppress
from typing import Any, Dict, Generator, List, Optional, Sequence
import consts as C
import yeelight as Y
# import dev.yeelight_dummy as Y  # For development purposes, replace with actual yeelight import in production
import logging
import yaml


logger = logging.getLogger(__name__)
CAPABILITIES = "capabilities"
ID = "id"
IP = "ip"
__discovered: Optional[Dict] = None


def get_discovered() -> List[Dict]:
    """
    Returns the discovered list of dictionaries describing bulbs.
    Else, queries the network for available bulbs.

    :return: List of Dicts or None
    """
    global __discovered
    if __discovered is None:
        try:
            logger.info("Discovering bulbs...")
            __discovered = Y.discover_bulbs()
            if len(__discovered) < 1:
                raise ValueError("No bulbs discovered.")
            for bulb in __discovered:
                logger.info(
                    f"Discovered bulb: {bulb[CAPABILITIES][ID]} at {bulb[IP]}")
        except Exception as e:
            logger.critical(f"Cannot discover bulbs: {str(e)}")
            raise ValueError(f"Cannot discover bulbs: {str(e)}")
    return __discovered


class MidiBulb(Y.Bulb):

    @staticmethod
    def get_ip_from_id(bulb_id: str) -> str:
        for bulb in get_discovered():
            if bulb[CAPABILITIES][ID] == bulb_id:
                return bulb["ip"]
        logger.critical(
            f"Bulb with ID {bulb_id} not found.\nRun wizard_configuration.py again.")
        raise ValueError(
            f"Bulb with ID {bulb_id} not found.\nRun wizard_configuration.py again.")

    def __init__(self, bulb_id: str) -> None:
        """
        MidiBuld class wraps around Yeelight's Bulb class, 
        providing additional functionality.\n
        It hides the IP address of the bulbs and allows
        to reach them just by their ID.

        :param bulb_id: ID of the bulb to connect to.
        """
        bulb_ip = MidiBulb.get_ip_from_id(bulb_id)
        super().__init__(bulb_ip, effect="sudden")
        self._ip: str = bulb_ip  # TODO might not be needed
        self._id: str = bulb_id
        self._sticker_id: Optional[str] = None
        self._channel: Optional[int] = None

    def __repr__(self) -> str:
        s = f"MidiBulb: {self.id=}, {self._ip=}, {self.sticker_id=}, {self.channel=}\n"
        return s

    @property
    def id(self) -> str:
        if self._id is None:
            logger.error(f"Cannot get ID of bulb")
            return "err"
        return self._id

    @property
    def sticker_id(self) -> str:
        if self._sticker_id is None:
            logger.error(f"Cannot get sticker ID of bulb")
            return "err"
        return self._sticker_id

    @sticker_id.setter
    def sticker_id(self, sticker_id: str) -> None:
        self._sticker_id = sticker_id
        return

    @property
    def channel(self) -> int:
        if self._channel is None:
            logger.error(f"Cannot get channel of bulb")
            return -1
        return self._channel

    @channel.setter
    def channel(self, ch: int) -> None:
        if (ch < 0) or (ch > C.CHANNEL_COUNT - 1):
            logger.error(
                f"Invalid channel {ch} for bulb {self.id}. Expected 0..{C.CHANNEL_COUNT - 1}, saturating to {C.CHANNEL_COUNT - 1}.")
            self._channel = C.CHANNEL_COUNT - 1
        self._channel = ch
        return

    @staticmethod
    def discover() -> List["MidiBulb"]:
        """
        Discover available bulbs and return a list of MidiBulb objects.
        """
        midi_bulbs = []
        for yeelight_bulb in get_discovered():
            midi_bulbs.append(MidiBulb(yeelight_bulb[CAPABILITIES][ID]))
        return midi_bulbs

    @contextmanager
    def distinguish(self) -> Generator[None, Any, None]:
        """
        Helper function, that lights up the bulb for context.

        :note: Utilizes `with` statement.
        """
        if self is None:
            logger.error(f"Cannot distinguish bulb {self.id}")
            return
        logger.info(
            f"Distinguishing bulb {self.id} with sticker ID {self.sticker_id} in channel {self.channel}.")
        self.turn_on()
        self.set_rgb(*C.DISTINGUISH_COLOR)
        self.set_brightness(100)
        yield
        self.turn_off()
        return


def to_yaml(bulb_in_channel: Dict[int, List[MidiBulb]], filename: str = "config.yml") -> None:
    yaml_formated = []
    for bulbs in bulb_in_channel.values():
        for bulb in bulbs:
            yaml_formated.append(
                {
                    "bulb_id": bulb.id,
                    "sticker": bulb.sticker_id,
                    "channel": bulb.channel
                }
            )
    with open(filename, "w+") as f:
        yaml.dump(yaml_formated, f)


def from_yaml(filename: str = "config.yml") -> Dict[int, List[MidiBulb]]:
    with open(filename, "r") as f:
        yaml_formated = yaml.safe_load(f)
    ret: Dict[int, List[MidiBulb]] = {}
    for yaml_bulb in yaml_formated:
        bulb_id = yaml_bulb["bulb_id"]
        sticker_id = yaml_bulb["sticker"]
        channel = int(yaml_bulb["channel"])
        if channel not in ret.keys():
            ret[channel] = []
        midibulb = MidiBulb(bulb_id)
        midibulb.sticker_id = sticker_id
        midibulb.channel = channel
        ret[channel].append(midibulb)
    return ret


@contextmanager
def distinguish_channel(bulbs: List[MidiBulb]) -> Generator[None, Any, None]:
    for bulb in bulbs:
        bulb.turn_on()
        bulb.set_rgb(*C.DISTINGUISH_COLOR)
        bulb.set_brightness(100)
    yield
    for bulb in bulbs:
        bulb.turn_off()
