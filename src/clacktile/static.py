from textual.reactive import reactive
from textual.widgets import Static

from clacktile.textloader import load_text


class StaticText(Static, can_focus=True):
    count = reactive(0)

    def __init__(self, id: str) -> None:
        super().__init__(renderable=load_text(0), id=id)

    def goto_text(self) -> None:
        print("action go to next ########")
        self.count += 1
        self.renderable = load_text(self.count)
