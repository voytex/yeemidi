"""

"""
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional, Sequence
import consts as C
#import yeelight as Y
import dev.yeelight_dummy as Y  # For development purposes, replace with actual yeelight import in production
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
                logger.info(f"Discovered bulb: {bulb[CAPABILITIES][ID]} at {bulb[IP]}")
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
        logger.critical(f"Bulb with ID {bulb_id} not found.\nRun wizard_configuration.py again.")
        raise ValueError(f"Bulb with ID {bulb_id} not found.\nRun wizard_configuration.py again.")


    def __init__(self, bulb_id: str) -> None:
        """
        """
        bulb_ip = MidiBulb.get_ip_from_id(bulb_id)
        super().__init__(bulb_ip)
        self._ip: str = bulb_ip # TODO might not be needed
        self._id: str = bulb_id
        self._sticker_id: Optional[str] = None
        self._group: Optional[int] = None


    def __repr__(self) -> str:
        s = "MidiBulb:\n"
        for k, v in self.__dict__.items():
            s += f"{k}: {v}\n"
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
    def group(self) -> int:
        if self._group is None:
            logger.error(f"Cannot get group of bulb")
            return -1
        return self._group
    

    @group.setter
    def group(self, group: int) -> None:
        if group < 0 or group > 16:
            logger.error(f"Invalid group {group} for bulb {self.id}. Expected 0..16, saturating to 16.")
            self._group = 16
        self._group = group
        return
        

    @staticmethod
    def to_yaml(bulbs_list: List["MidiBulb"], filename: str) -> None:
        """
        """
        yaml_list = []
        for bulb in bulbs_list:
            yaml_list.append({
                "id": bulb.id,
                "sticker_id": bulb._sticker_id,
                "group": bulb._group,
            })
        with open(filename, "w") as f:
            yaml.dump(yaml_list, f)
        return
    

    @staticmethod
    def from_yaml(filename: str) -> List["MidiBulb"]:
        """
        """
        try:
            with open(filename, "r") as f:
                yaml_list = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Cannot load yaml file: {filename}\n{str(e)}")
            print(f"Cannot load yaml file: {filename}\n{str(e)}")
            return []
        bulbs_list = []
        for bulb in yaml_list:
            # TODO IP handling
            obj = MidiBulb(bulb["id"])
            obj._sticker_id = bulb["sticker_id"]
            obj._group = bulb["group"]
            bulbs_list.append(obj)
        return bulbs_list

    
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
        logger.info(f"Distinguishing bulb {self.id} with sticker ID {self.sticker_id} in group {self.group}.")
        self.set_rgb(*C.DISTINGUISH_COLOR)
        self.set_brightness(100)
        self.turn_on()
        yield
        self.turn_off()
        self.set_brightness(0)
        self.set_rgb(0, 0, 0)
        return
    

class MidiBulbCollection:
    class _Group(Y.Bulb):
        def add(self, bulbs: Sequence[MidiBulb], ensure_music_mode: bool = True) -> None:
            self.bulbs: List[MidiBulb] = []
            for bulb in bulbs:
                if ensure_music_mode:
                    bulb.start_music()
                self.bulbs.append(bulb)
            return
        
        def __init__(self) -> None:
            pass

        def __getattr__(self, name: str):
            def method(*args, **kwargs):
                for bulb in self.bulbs:
                    attr = getattr(bulb, name)
                    if callable(attr):
                        attr(*args, **kwargs)
                    else:
                        logger.error(f"Attribute {name} is not callable on {bulb.id}.")
            return method

        def __iter__(self):
            return iter(self.bulbs)
        
        def __len__(self) -> int:
            return len(self.bulbs)
        
        def __getitem__(self, index: int) -> MidiBulb:
            return self.bulbs[index]
        
        @contextmanager
        def distinguish(self) -> Generator[None, Any, None]:
            logger.info(f"Distinguishing group.")
            for bulb in self.bulbs:
                bulb.set_rgb(*C.DISTINGUISH_COLOR)
                bulb.set_brightness(100)
                bulb.turn_on()
            yield
            for bulb in self.bulbs:
                bulb.turn_off()
                bulb.set_brightness(0)
                bulb.set_rgb(0, 0, 0)
            return
        
    
    def __init__(self, no_of_groups: int) -> None:
        if no_of_groups < 1 or no_of_groups > 16:
            logger.error(f"Invalid number of groups: {no_of_groups}. Expected 1..16, saturating to 16.")
            no_of_groups = 16
        self.group: List[MidiBulbCollection._Group] = no_of_groups * [MidiBulbCollection._Group()]


    def __getitem__(self, group_no: int) -> _Group:
        """
        Returns the list of MidiBulbs in the specified group.
        """
        return self.group[group_no]
        



        

    
