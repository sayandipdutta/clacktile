from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from clacktile.textloader import load_text


class StaticText(Static, can_focus=True):
    count = reactive(0)

    class Changed(Message):
        pass

    def __init__(self, id: str) -> None:
        super().__init__(renderable=load_text(0), id=id)

    def next(self) -> None:
        self.count += 1
        self.renderable = load_text(self.count)
        self.post_message(self.Changed())
