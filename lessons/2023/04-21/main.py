import click
from client import Client
from config import Config
from logger import Log
from server import Server
from ui import UI


@click.group()
def cli():
    pass


@cli.command("client")
@click.option(
    "-c",
    "--config",
    help="The configuration file must be in YAML format",
)
@click.option("-n", "--name", help="Your name in the chat", type=str)
@click.option("-s", "--host", help="Hostname (or IP) of the YACR Server", type=str)
@click.option("-p", "--port", help="TCP port of the YACR Server", type=int)
def start_client(config: str, name: str, host: str, port: int) -> None:
    log: Log = Log(filename="log/yacr-client.log")

    cfg: Config = Config(
        log=log,
        path=config,
        data={"name": name, "server.host": host, "server.port": port},
    )

    client: Client = Client(log=log)
    client.start(name=cfg.name, host=cfg.host, port=cfg.port)

    ui: UI = UI(socket=client, log=log, name=cfg.name)
    ui.run()


@cli.command("server")
@click.option(
    "-c",
    "--config",
    default="server.yaml",
    help="The configuration file must be in YAML format",
)
@click.option("-s", "--host", help="Hostname (or IP) of the YACR Server", type=str)
@click.option("-p", "--port", help="TCP port of the YACR Server", type=int)
def start_server(config: str, host: str, port: int) -> None:
    log: Log = Log(filename="log/yacr-server.log")

    cfg: Config = Config(
        log=log,
        path=config,
        data={"server.host": host, "server.port": port},
    )

    server: Server = Server(log=log)
    server.start(host=cfg.host, port=cfg.port)


if __name__ == "__main__":
    cli()
