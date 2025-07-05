from yeelight.flow import Flow, Action, TemperatureTransition, RGBTransition, SleepTransition
from typing import List, Optional
import logging


logger = logging.getLogger(__name__)


DEFAULT_FLOW: Flow = Flow(1, Action.off, [SleepTransition(50)])
FLOW_TABLE: List[Optional[Flow]] = [None for _ in range(1,128)]
FLOW_TABLE[1] = Flow(
    # Strobo
    0, Action.off, [
        TemperatureTransition(3500, 50, 50),
        SleepTransition(50),
        TemperatureTransition(3500, 50, 1),
        SleepTransition(50)
    ]
)
FLOW_TABLE[2] = Flow(
    0, Action.off, [
        RGBTransition(24, 10, 235, 1000, 100),
        RGBTransition(128, 72, 2, 1000, 1),
    ]
)

def get_flow(num: int) -> Flow:
    try:
        return FLOW_TABLE[num]
    except Exception:
        logger.error(f"Flow {num=} not present in FLOW_TABLE")
        return DEFAULT_FLOW