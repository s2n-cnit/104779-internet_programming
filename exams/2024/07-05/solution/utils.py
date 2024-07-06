import logging

logging.getLogger("passlib").setLevel(logging.ERROR)
logger = logging.getLogger("Test")


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
