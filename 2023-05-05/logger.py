from __future__ import annotations

import sys

from loguru import logger


class Log:
    def __init__(self: Log, filename: str = None) -> None:
        logger.remove()
        self.__log = logger
        self.__log.remove()
        self.__log.add(
            sink=sys.stdout,
            format="[{time:HH:mm:ss}] <lvl>{message}</lvl>",
            level="DEBUG",
        )
        if filename is not None:
            self.__log.add(
                filename, format="{name} {message}", level="DEBUG", rotation="5 MB"
            )
        self.success = self.__log.success
        self.warning = self.__log.warning
        self.info = self.__log.info
        self.debug = self.__log.debug
        self.error = self.__log.error

    def exception(
        self: Log,
        message: str,
        error: any = None,
        exception: any = None,
        terminate: bool = True,
    ) -> None:
        self.error(message)
        if error is not None:
            self.debug(f"Error: {error}")
        if exception is not None:
            self.debug(f"Exception: {exception}")
        if terminate:
            sys.exit()
