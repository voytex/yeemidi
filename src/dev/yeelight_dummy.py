import logging, time

logger = logging.getLogger(__name__)


class Bulb:
    def __init__(self, *args, ):
        pass

    def __getattr__(self, name):
        logger.info(f"Accessed attribute or method: {name}")
        return self

    def __call__(self, *args, **kwargs):
        logger.info(f"Called with args: {args}, kwargs: {kwargs}")
        return self

def discover_bulbs():
    """
    Dummy function to simulate bulb discovery.
    """
    logger.info("Discovering bulbs...")
    time.sleep(1)
    return [{"capabilities": {"id": "0x0000000002dfb19a"}, "ip": "10.10.0.1"},{"capabilities": {"id": "0x0000000002dfb13f"}, "ip": "10.10.0.2"}]