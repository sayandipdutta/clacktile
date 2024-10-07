from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from textual.events import Key
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import TextArea


class Status(Enum):
    NOT_STARTED = auto()
    STARTED = auto()
    ENDED = auto()


class TypingArea(TextArea):
    typing_status = reactive(Status.NOT_STARTED)

    @dataclass
    class StatusChanged(Message):
        status: Status

    def __init__(self, text: str = "", *, id: str | None = None) -> None:
        super().__init__(text, show_line_numbers=False, id=id)

    def reset(self):
        _ = self.clear()
        self.typing_status = Status.NOT_STARTED

    def on_key(self, key: Key):
        if key.is_printable and self.typing_status is Status.NOT_STARTED:
            self.typing_status = Status.STARTED

    def on_counter_status_changed(self, status: str):
        if status == "ended":
            self.typing_status = Status.ENDED

    def watch_typing_status(self, status: Status):
        match status:
            case Status.STARTED:
                _ = self.post_message(TypingArea.StatusChanged(status))
            case Status.ENDED:
                _ = self.post_message(TypingArea.StatusChanged(status))
                self.read_only = True
            case _:
                pass
