from __future__ import annotations

from dataclasses import dataclass
from typing import cast
from textual.events import Key
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import TextArea

from clacktile.common import Status


class TypingArea(TextArea):
    typing_status = reactive(Status.NOT_STARTED)

    @dataclass
    class StatusChanged(Message):
        status: Status
        text: str

    @dataclass
    class Editing(Message):
        text: str

    def __init__(self, text: str = "", *, id: str | None = None) -> None:
        super().__init__(text, show_line_numbers=False, id=id)

    def reset(self):
        self.typing_status = Status.NOT_STARTED

    def on_key(self, key: Key):
        char = cast(str, key.character if key.is_printable else "")
        editing_key = char or key.key in ("backspace", "delete")
        if self.typing_status is Status.NOT_STARTED and char:
            self.typing_status = Status.STARTED

        if self.typing_status is not Status.ENDED and editing_key:
            _ = self.post_message(self.Editing(text=self.text + char))

    def watch_typing_status(self, status: Status):
        self.read_only = status is Status.ENDED
        match status:
            case Status.STARTED | Status.ENDED:
                _ = self.post_message(self.StatusChanged(status, text=self.text))
            case Status.NOT_STARTED:
                _ = self.clear()
