import ast
import os
import signal
import sys
import threading
from enum import Enum
from subprocess import PIPE, run
from threading import Thread
from typing import Dict, Optional, Self, Type


class Struct:
    """Emulate the stdclass of PHP."""

    def __init__(self: Self, **entries: Dict[str, any]) -> None:
        """Create all the data members based on the keyword arguments.

        Parameters:
        self (Struct) -- this object
        entries (Dict[str, any]) -- key/value sequence for the variables to
        create as data-member of this object
        """
        self.__dict__.update(entries)


def threaded(func: callable) -> Thread:
    """Decorator that multithreading the target function
    with the given parameters.

    Parameters:
    func (callable) -- to execute in a separate thread

    Returns:
    Thread:Created for the function
    """

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args)
        thread.start()
        return thread

    return wrapper


class EnumList(Enum):
    """Add to Enum a method to get the list of all the values."""

    @classmethod
    def list(cls: Type[Self]):
        """All values of this enum as list

        Parameters
        cls -- class type

        Returns:
        list:Returning all the values.
        """
        return list(map(lambda c: c.value, cls))


def execute(cmd: str, logger: any, min_lines_warning: int) -> int:
    """
    Execute a program and write with the logger the result.

    Parameters
    cmd (str) -- Command to execute
    logger (any) -- To write the output
    min_lines_warning (int) -- Minimum number of lines to log as warning

    Returns:
    int:Return code of the command
    """
    _result = run(
        cmd,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
        shell=True,
    )
    _res_lines = list(filter(None, _result.stdout.split("\n")))
    if _result.returncode != 0:
        _callback = logger.error
    elif len(_res_lines) >= min_lines_warning:
        _callback = logger.warning
    else:
        _callback = logger.success
    for r in _res_lines:
        _callback(r)
    return _result.returncode


def keyboard_interrupt(
    callback: callable, return_code: Optional[int] = 0, waiting: bool = True
) -> None:
    """Manage the interruption of a script execution with the keyboard press
    event.

    Parameters
    callback (callable) -- executed after the interruption
    return_code (int | None) -- if not None exit the program with this code
    waiting (bool) -- to wait the keyword interruption.
    """

    def _handler(signal, frame):
        print("\r", end="")  # To present "^C" in the stdout.
        callback()
        if return_code is not None:
            sys.exit(return_code)

    signal.signal(signal.SIGINT, _handler)
    if waiting:
        _forever = threading.Event()
        _forever.wait()


def get_classes(file_path: str, with_module_name: bool = False):
    if file_path.endswith(".py"):
        with open(file_path, "r") as _src:
            _parse = ast.parse(_src.read())
            if with_module_name:
                module_name, _ = os.path.splitext(os.path.basename(file_path))
                _with_module_name = f"{module_name}."
            else:
                _with_module_name = ""
            return [
                f"{_with_module_name}{node.name}" for node in ast.walk(_parse)
                if isinstance(node, ast.ClassDef)
            ]
    else:
        raise SyntaxError(f"{file_path} not valid")


def nothing():
    pass


def exit_handler(logger: any, additional_callback: callable = nothing):
    def _exit():
        logger.warning("Terminating...")
        additional_callback()

    return _exit
