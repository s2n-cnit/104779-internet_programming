from __future__ import annotations

from socket import AF_INET, SOCK_STREAM
from socket import error as SocketError
from socket import socket as Socket

from logger import Log

DEFAULT_HOST: str = "localhost"
DEFAULT_PORT: int = 32000


class SocketExtended:
    def __init__(self: SocketExtended, log: Log) -> None:
        self._log: Log = log
        try:
            # create a TCP socket (SOCK_STREAM)
            self._socket: Socket = Socket(family=AF_INET, type=SOCK_STREAM, proto=0)
            self._log.success("Socket created")
            self.send = self._socket.send
            self.recv = self._socket.recv
            self.close = self._socket.close
        except SocketError as socket_err:
            self._log.exception("Error during creation of the socket", error=socket_err)
