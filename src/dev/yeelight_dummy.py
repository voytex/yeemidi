import logging

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
