import json
from threading import Thread

import pglet
import redis
from config import Config
from logger import Log
from pglet import Button, Checkbox, Textbox


def main(page):
    log = Log("yacr-web.log")
    config = Config(log, path="config.yaml")
    red = redis.StrictRedis(
        config.host,
        config.port,
        charset="utf-8",
        decode_responses=True,
    )

    msg = Textbox(label=config.name)

    def send_msg(e):
        try:
            red.publish(
                "yacr",
                json.dumps(dict(name=config.name, message=msg.value)),
            )
        except ConnectionError as conn_err:
            log.exception(
                f"Connection error with pubsub system located at {config.host}:{config.port}",
                conn_err,
            )

    def receive_msg():
        while True:
            try:
                sub = red.pubsub()
                sub.subscribe("yacr")
            except redis.exceptions.ConnectionError as conn_err:
                log.exception(
                    f"Connection error with pubsub system located at {config.host}:{config.port}",
                    conn_err,
                )
            for message in sub.listen():
                if message is not None and isinstance(message, dict):
                    data = message.get("data")
                    if isinstance(data, int):
                        continue
                    data = json.loads(data)
                    print(data)

    t: Thread = Thread(target=receive_msg)
    t.daemon = True
    # t.start()

    page.add(msg, Button("Send", on_click=send_msg))


pglet.app("yacr", target=main)
