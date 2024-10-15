from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from clacktile.textloader import SavedTexts


class StaticText(Static, can_focus=True):
    count = reactive(0)

    class Changed(Message):
        pass

    def __init__(self, id: str) -> None:
        super().__init__(renderable=SavedTexts.load(0), id=id)

    def next(self) -> None:
        self.count += 1
        self.renderable = SavedTexts.load(self.count)
        _ = self.post_message(self.Changed())
