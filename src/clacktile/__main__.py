from pathlib import Path
from random import choice
from typing import Final

from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Header, Static


SAVED_TEXT_PATH: Final[Path] = Path(__file__).parent / "saved"


def load_random_text() -> str:
    chosen_file = choice(list(SAVED_TEXT_PATH.glob("*.txt")))
    return chosen_file.read_text()


class LayersExample(App):
    CSS_PATH = "style/layers.tcss"
    TITLE = "Clacktile"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Center():
                yield Static(load_random_text(), id="text")
            with Center():
                yield Static("input", id="input")


# if __name__ == "__main__":
app = LayersExample()
# app.run()
