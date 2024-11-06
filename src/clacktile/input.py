from __future__ import annotations

from dataclasses import dataclass
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

    def __init__(self, text: str = "", *, id: str | None = None) -> None:
        super().__init__(text, show_line_numbers=False, id=id)

    def reset(self):
        self.typing_status = Status.NOT_STARTED

    def on_key(self, key: Key):
        if key.is_printable and self.typing_status is Status.NOT_STARTED:
            self.typing_status = Status.STARTED

    def watch_typing_status(self, status: Status):
        match status:
            case Status.STARTED:
                _ = self.post_message(TypingArea.StatusChanged(status, text=self.text))
                self.read_only = False
            case Status.ENDED:
                # TODO: Consider cursor visibility
                self.read_only = True
                _ = self.post_message(self.StatusChanged(Status.ENDED, text=self.text))
            case Status.NOT_STARTED:
                _ = self.clear()
