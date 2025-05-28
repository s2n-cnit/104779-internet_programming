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
        for k, v in data.items():
            if v is not None:
                r: Dict[str, any] = self.__config
                keys: List[str] = k.split(".")
                for sk in keys[:-1]:
                    r = r[sk]
                r[keys[-1]] = v
        self.__path: str = path

    def __get(self: Config, *keys: List[str]) -> any:
        try:
            cfg: Dict[str, any] = self.__config
            for key in keys:
                cfg = cfg[key]
            return cfg
        except KeyError as k_err:
            self.__log.exception(
                f"{'.'.join(keys)} not found in config {self.__path}", error=k_err
            )

    @property
    def host(self: Config) -> str:
        return self.__get("server", "host")

    @property
    def port(self: Config) -> int:
        return self.__get("server", "port")

    @property
    def name(self: Config) -> str:
        return self.__get("name")
