import click
from config import Config
from logger import Log
from ui import UI


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
    log: Log = Log(filename="log/yacr-redis.log")

    cfg: Config = Config(
        log=log,
        path=config,
        data={"name": name, "server.host": host, "server.port": port},
    )

    ui: UI = UI(log=log, config=cfg)
    ui.run()


if __name__ == "__main__":
    main()
