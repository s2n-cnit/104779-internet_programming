from __future__ import annotations

from typing import Dict, List

import yaml
from logger import Log


class Config:

    def __init__(
        self: Config, log: Log, path: str = None, data: Dict[str, any] = dict()
    ) -> None:
        self.__config = {}
        self.__log: Log = log
        try:
            if path is not None:
                self.__config = yaml.safe_load(open(path, "r"))
        except FileNotFoundError as fnf_err:
            self.__log.exception(f"File {path} not found", error=fnf_err)
        self.__config.update(data)
        self.__path: str = path

    @property
    def host(self: Config) -> str:
        return self.__config["server"]["host"]

    @property
    def port(self: Config) -> int:
        return self.__config["server"]["port"]

    @property
    def name(self: Config) -> str:
        return self.__config["name"]
