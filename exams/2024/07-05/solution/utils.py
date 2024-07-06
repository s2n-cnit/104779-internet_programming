import logging
from threading import Thread

logging.getLogger("passlib").setLevel(logging.ERROR)
logger = logging.getLogger("Test")


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def threaded(func):
    """
    Decorator that multithreading the target function
    with the given parameters. Returns the thread
    created for the function
    """

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args)
        thread.start()
        return thread

    return wrapper
