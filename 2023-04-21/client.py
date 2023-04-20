from __future__ import annotations

from threading import Thread

import click
from config import Config
from logger import Log
from socket_extended import DEFAULT_HOST, DEFAULT_PORT, SocketExtended
from ui import UI


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


@click.command()
@click.option(
    "-c",
    "--config",
    help="The configuration file must be in YAML format",
)
@click.option("-n", "--name", help="Your name in the chat", type=str)
@click.option("-s", "--host", help="Hostname (or IP) of the Chat Room Server", type=str)
@click.option("-p", "--port", help="TCP port of the Chat Room Server", type=int)
def main(config: str, name: str, host: str, port: int) -> None:
    log: Log = Log(filename="yacr-client.log")

    cfg: Config = Config(
        log=log,
        path=config,
        data={"name": name, "server.host": host, "server.port": port},
    )

    client: Client = Client(log=log)
    client.start(name=cfg.name, host=cfg.host, port=cfg.port)

    ui: UI = UI(socket=client, log=log, name=cfg.name)
    ui.run()


main()
