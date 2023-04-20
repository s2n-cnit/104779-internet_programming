from __future__ import annotations

import sys
from threading import Thread

from logger import Log
from prompt_toolkit import HTML
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea
from socket_extended import SocketExtended


class UI:
    help_text = """
YACR (Yet Another Chat Room)
Type \"end\" to terminate.
"""

    def __init__(self, socket: SocketExtended, log: Log, name: str) -> None:
        self.__log = log
        self.__socket: SocketExtended = socket
        self.__name: str = name
        self.__output_field: TextArea = TextArea(
            style="class:output-field", text=UI.help_text
        )
        self.__search_field: SearchToolbar = SearchToolbar()  # For reverse search.
        self.__input_field: TextArea = TextArea(
            height=1,
            prompt=f"{name} >>> ",
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

    def run(self: UI) -> None:
        t: Thread = Thread(target=self.__write)
        t.daemon = True
        t.start()
        self.__app.run()

    def __accept(self, _: any) -> None:
        if self.__input_field.text.lower().strip() == "end":
            sys.exit(0)
        new_text = (
            f"{self.__output_field.text}\n{self.__name} > {self.__input_field.text}"
        )
        self.__output_field.buffer.document = Document(
            text=new_text, cursor_position=len(new_text)
        )
        self.__socket.send(self.__input_field.text.encode())

    def __write(self: UI) -> None:
        msg: str = None
        while msg != "":
            try:
                msg = self.__socket.recv(200).decode()
                new_text = self.__output_field.text + "\n" + msg
                self.__output_field.buffer.document = Document(
                    text=new_text, cursor_position=len(new_text)
                )
            except OSError as os_err:
                self.__log.exception(
                    "Error during reception of messages from server", error=os_err
                )
