from pathlib import Path
from typing import Final

from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Header, Static


SAVED_TEXT_PATH: Final[Path] = Path(__file__).parent / "saved"


def load_text() -> str:
    for file in SAVED_TEXT_PATH.glob("*.txt"):
        return file.read_text()
    else:
        return "No file available!"


class LayersExample(App):
    CSS_PATH = "style/layers.tcss"
    TITLE = "Clacktile"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Center():
                yield Static(load_text(), id="text")
            with Center():
                yield Static("input", id="input")


# if __name__ == "__main__":
app = LayersExample()
# app.run()
