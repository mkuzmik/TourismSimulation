import logging


def setup() -> None:
    logging.basicConfig(level=logging.DEBUG, format='[%(relativeCreated)6d] [%(threadName)s] %(message)s')
