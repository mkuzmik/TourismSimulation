import logging


def setup() -> None:
    logging.basicConfig(level=logging.INFO, format='[%(relativeCreated)6d] [%(threadName)s] %(message)s')
