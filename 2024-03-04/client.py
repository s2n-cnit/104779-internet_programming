from __future__ import annotations

from logger import Log
from socket_extended import DEFAULT_HOST, DEFAULT_PORT, SocketExtended


class Client(SocketExtended):
    def __init__(self: SocketExtended, log: Log) -> None:
        super().__init__(log)

    def start(
        self: Client,
        name: str,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
    ) -> None:
        try:
            self._socket.connect((host, port))
            self._log.success(f"Connected to the server {host}:{port}")
        except ConnectionRefusedError as cr_err:
            self._log.exception(
                f"Connection refused from the server {host}:{port}", error=cr_err
            )
        except TimeoutError as to_err:
            self._log.exception(
                f"Timeout error during connection to the server {host}:{port}",
                error=to_err,
            )

        self.__host: str = host
        self.__port: int = port
        self.__name = name
        self._socket.send(name.encode())
