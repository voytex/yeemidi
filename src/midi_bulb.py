"""

"""
from contextlib import contextmanager
from typing import Any, Dict, Generator, List, Optional
import consts as C
if C.DEV:
    import dev.yeelight_dummy as Y 
else:
    import yeelight as Y
import logging
import yaml


logger = logging.getLogger(__name__)


class WrappedBulb:

    def __init__(self) -> None:
        """
        """
        self._bulb: Optional[Y.Bulb] = None
        self._id: Optional[str] = None
        self._ip: Optional[str] = None
        self._sticker_id: Optional[str] = None
        self._group: Optional[int] = None


    def __repr__(self) -> str:
        s = "WrappedBulb:\n"
        for k, v in self.__dict__.items():
            s += f"{k}: {v}\n"
        return s


    @staticmethod
    def from_yeelight(bulb: Y.Bulb) -> "WrappedBulb":
        """
        """
        obj = WrappedBulb()
        obj._bulb = bulb
        obj._ip = bulb.get_properties()["ip"]
        obj._id = bulb.get_properties()["id"]
        return obj


    @staticmethod
    def from_dict(dict: Dict) -> Optional["WrappedBulb"]:
        """
        :param dict: Dict to be converted to WrappedBulb.
        :return: WrappedBulb or None if cannot be instantiated.
        """
        try: 
            obj = WrappedBulb()
            obj._bulb = Y.Bulb(dict["ip"])
            obj._ip = dict["ip"]
            obj._id = dict["capabilities"]["id"]
            return obj
        except Exception as e:
            logger.error(f"Cannot instaniate WrappedBulb from dict: {dict}\n{str(e)}")
            return None
        

    @staticmethod
    def to_yaml(bulbs_list: List["WrappedBulb"], filename: str) -> None:
        """
        """
        yaml_list = []
        for bulb in bulbs_list:
            yaml_list.append({
                "ip": bulb._ip,
                "id": bulb._id,
                "sticker_id": bulb._sticker_id,
                "group": bulb._group,
            })
        with open(filename, "w") as f:
            yaml.dump(yaml_list, f)
        return
    

    @staticmethod
    def from_yaml(filename: str) -> List["WrappedBulb"]:
        """
        """
        try:
            with open(filename, "r") as f:
                yaml_list = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Cannot load yaml file: {filename}\n{str(e)}")
            print(f"Cannot load yaml file: {filename}\n{str(e)}")
        bulbs_list = []
        for bulb in yaml_list:
            obj = WrappedBulb()
            obj._ip = bulb["ip"]
            obj._id = bulb["id"]
            obj._sticker_id = bulb["sticker_id"]
            obj._group = bulb["group"]
            bulbs_list.append(obj)
        return bulbs_list
        

    @property
    def id(self) -> str:
        if self._id: return self._id
        else:
            logger.error(f"Cannot access ID of this bulb")
            return "err"
        
    @property
    def ip(self) -> str:
        if self._ip: return self._ip
        else:
            logger.error(f"Cannot access IP of this bulb")
            return "err"
        
    @property
    def sticker_id(self) -> str:
        if self._sticker_id: return self._sticker_id
        else:
            logger.error(f"Cannot access sticker ID of this bulb")
            return "err"
        
    @sticker_id.setter
    def sticker_id(self, sticker_id: str) -> None:
        self._sticker_id = sticker_id
        return 
    
    @property
    def group(self) -> int:
        if self._group: return self._group
        else:
            logger.error(f"Cannot access group of this bulb")
            return -1
        
    @group.setter
    def group(self, group: int) -> None:
        self._group = group
        return
    
    @contextmanager
    def distinguish(self) -> Generator[None, Any, None]:
        """
        """
        if self._bulb is None:
            logger.error(f"Cannot distinguish bulb {self._id}")
            return
        self._bulb.set_brightness(100)
        self._bulb.set_rgb(*C.DISTINGUISH_COLOR)
        yield
        self._bulb.set_brightness(0)
        self._bulb.set_rgb(0, 0, 0)
        return
        
