from pathlib import Path
from typing import Final

from textual.reactive import reactive
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Center, Vertical
from textual.widget import Widget
from textual.widgets import Header, Static


SAVED_TEXT_PATH: Final[Path] = Path(__file__).parent / "saved"


def load_text(index: int) -> str:
    files = list(SAVED_TEXT_PATH.glob("*.txt"))
    if not files:
        return "No files available!"
    index %= len(files)
    return files[index].read_text()


class TextArea(Static, can_focus=True):
    BINDINGS = [
        ("right,l", "goto_text(1)", "Next"),
        ("left,h", "goto_text(-1)", "Previous"),
    ]

    count = reactive(0)
    text = reactive(load_text(0))

    def render(self) -> RenderResult:
        return self.text

    def action_goto_text(self, amount: int) -> None:
        self.count += amount
        self.text = load_text(self.count)


# class TypingArea(Widget):
#     CSS_PATH = "style/typing.tcss"
#
#     def compose(self) -> ComposeResult: ...


class ClacktileApp(App):
    CSS_PATH = "style/layers.tcss"
    TITLE = "Clacktile"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Center():
                yield TextArea(id="text")
            with Center():
                yield Static("typing", id="input")


if __name__ == "__main__":
    app = ClacktileApp()
    app.run()
