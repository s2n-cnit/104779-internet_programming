from __future__ import annotations

import json
import sys
from datetime import datetime
from threading import Thread

import redis
from config import Config
from logger import Log
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea


class UI:
    help_text = """
YACR (Yet Another Chat Room)
Type \"end\" to terminate.
"""

    def __init__(self: UI, log: Log, config: Config) -> None:
        self.__log = log
        self.__config = config
        self.__output_field: TextArea = TextArea(
            style="class:output-field", text=UI.help_text
        )
        self.__search_field: SearchToolbar = SearchToolbar()  # For reverse search.
        self.__input_field: TextArea = TextArea(
            height=1,
            prompt=f"{self.__config.name} >>> ",
            style="class:input-field",
            multiline=False,
            wrap_lines=False,
            search_field=self.__search_field,
        )
        self.__input_field.accept_handler = self.__accept
        self.__container: HSplit = HSplit(
            [
                self.__output_field,
                Window(height=1, char="-", style="class:line"),
                self.__input_field,
            ]
        )
        self.__layout: Layout = Layout(
            self.__container, focused_element=self.__input_field
        )
        self.__style = Style(
            [("input-field", "fg:ansired"), ("output-field", "fg:#00aaaa")]
        )
        self.__app: Application = Application(
            layout=self.__layout,
            style=self.__style,
            color_depth=ColorDepth.DEPTH_24_BIT,
            full_screen=True,
        )
        self.__redis = redis.StrictRedis(
            self.__config.host,
            self.__config.port,
            charset="utf-8",
            decode_responses=True,
        )
        self.__publish(type="!", message="joins the chat")

    def run(self: UI) -> None:
        t: Thread = Thread(target=self.__write, kwargs={"private": False})
        t.daemon = True
        t.start()
        t_private: Thread = Thread(target=self.__write, kwargs={"private": True})
        t_private.daemon = True
        t_private.start()
        self.__app.run()

    def __publish(self: UI, type: str, message: str) -> None:
        try:
            message = message.strip()
            if message != "":
                if message.startswith("@"):
                    message = message[1:]
                    c = message.split(" ")
                    message = " ".join(c[1:])
                    topic = [f"yacr-{c[0]}", f"yacr-{self.__config.name}"]
                    type = ["*", f"*{c[0]}"]
                else:
                    topic = ["yacr"]
                    type = [type]
                for i, tp in enumerate(topic):
                    self.__redis.publish(
                        tp,
                        json.dumps(
                            dict(
                                name=self.__config.name,
                                type=type[i],
                                message=message,
                                time=str(datetime.now()),
                            )
                        ),
                    )
        except ConnectionError as conn_err:
            self.__log.exception(
                f"Connection error with pubsub system located at {self.__config.host}:{self.__config.port}",
                conn_err,
            )

    def __accept(self, _: any) -> None:
        if self.__input_field.text.lower().strip() == "end":
            self.__publish(type="!", message="leaves the chat")
            sys.exit(0)
        else:
            self.__publish(type=">", message=self.__input_field.text)

    def __write(self: UI, private: bool) -> None:
        while True:
            try:
                sub = self.__redis.pubsub()
                if private:
                    sub.subscribe(f"yacr-{self.__config.name}")
                else:
                    sub.subscribe("yacr")
            except redis.exceptions.ConnectionError as conn_err:
                self.__log.exception(
                    f"Connection error with pubsub system located at {self.__config.host}:{self.__config.port}",
                    conn_err,
                )
            for message in sub.listen():
                if message is not None and isinstance(message, dict):
                    data = message.get("data")
                    if isinstance(data, int):
                        continue
                    data = json.loads(data)
                    new_text = f'{self.__output_field.text}\n{data["name"]} {data["type"]} {data["message"]} at {data["time"]}'
                    self.__output_field.buffer.document = Document(
                        text=new_text, cursor_position=len(new_text)
                    )
