from __future__ import annotations

from datetime import datetime
from socket import SO_REUSEADDR, SOL_SOCKET
from socket import socket as Socket
from threading import Thread
from typing import List

from logger import Log
from socket_extended import DEFAULT_HOST, DEFAULT_PORT, SocketExtended


class Server(SocketExtended):
    def __init__(self: SocketExtended, log: Log) -> None:
        super().__init__(log)

    def start(
        self: Server,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
    ) -> None:
        self._socket.bind((host, port))
        self._socket.listen(5)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__host: str = host
        self.__port: int = port
        self.__client_sockets: List[Socket] = []
        while True:
            self._log.info(f"Waiting for incoming connection at {host}:{port}")
            client_socket, _ = self._socket.accept()
            self.__client_sockets.append(client_socket)
            client_name = client_socket.recv(200).decode()
            d = datetime.now()
            message = f"{client_name} ({d}) joined the chat"
            self._log.success(message)
            self.__dispatch_to_others(message)
            t: Thread = Thread(
                target=self.__process,
                kwargs={"name": client_name, "socket": client_socket},
            )
            t.daemon = True
            t.start()

    def __process(self: Server, name: str, socket: Socket) -> None:
        while True:
            msg = socket.recv(200).decode()
            if msg == "end":
                self.__client_sockets.remove(socket)
                socket.close()
                break
            else:
                d = datetime.now()
                self._log.success(f'{name} sends the message "{msg}"')
                self.__dispatch_to_others(f"{name} ({d})> {msg}")
        msg = f"{name} leaves the chat"
        self._log.warning(msg)
        for client_socket in self.__client_sockets:
            try:
                client_socket.send(msg.encode())
            except BrokenPipeError:
                pass

    def __dispatch_to_others(self: Server, message: str) -> None:
        for client_socket in self.__client_sockets:
            try:
                client_socket.send(message.encode())
            except OSError:
                pass
