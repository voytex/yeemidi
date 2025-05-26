"""

"""
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional
import consts as C
if not C.DEV:
    import yeelight as Y
else:
    import dev.yeelight_dummy as Y
import logging
import yaml


logger = logging.getLogger(__name__)


class MidiBulb(Y.Bulb):

    def __init__(self, bulb_dict: Dict) -> None:
        """
        """
        super().__init__(bulb_dict["ip"])
        self._ip: Optional[str] = bulb_dict["ip"]
        self._id: Optional[str] = bulb_dict["capabilities"]["id"]
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
    def ip(self) -> str:
        if self._ip is None:
            logger.error(f"Cannot get IP of bulb")
            return "err"
        return self._ip
    

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
                "ip": bulb.ip,
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
            obj = MidiBulb(bulb["ip"])
            obj._sticker_id = bulb["sticker_id"]
            obj._group = bulb["group"]
            bulbs_list.append(obj)
        return bulbs_list

    
    @contextmanager
    def distinguish(self) -> Generator[None, Any, None]:
        """
        Helper function, that lights up the bulb for context.

        :note: Utilizes `with` statement.
        """
        if self is None:
            logger.error(f"Cannot distinguish bulb {self._id}")
            return
        self.set_rgb(*C.DISTINGUISH_COLOR)
        self.set_brightness(100)
        self.turn_on()
        yield
        self.turn_off()
        self.set_brightness(0)
        self.set_rgb(0, 0, 0)
        return
        
