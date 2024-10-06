from pathlib import Path
from typing import Final

from textual.app import App, ComposeResult, RenderResult
from textual.containers import Center, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.suggester import Suggester
from textual.widgets import Header, Input, Static

SAVED_TEXT_PATH: Final[Path] = Path(__file__).parent / "saved"


def load_text(index: int) -> str:
    files = list(SAVED_TEXT_PATH.glob("*.txt"))
    if not files:
        return "No files available"
    index %= len(files)
    return files[index].read_text()


class TextArea(Static, can_focus=True):
    BINDINGS = [
        ("right,l", "goto_text(1)", "Next"),
        ("left,h", "goto_text(-1)", "Previous"),
    ]

    count = reactive(0)
    text = reactive(load_text(0))

    class TextChanged(Message):
        def __init__(self, text: str) -> None:
            self.text = text
            super().__init__()

    def render(self) -> RenderResult:
        return self.text

    def action_goto_text(self, amount: int) -> None:
        self.count += amount
        self.text = load_text(self.count)
        self.post_message(self.TextChanged(self.text))
        StaticSuggester.current_text = self.text


class TypingArea(Input):
    def action_cursor_right(self) -> None:
        self.cursor_position += 1


class StaticSuggester(Suggester):
    current_text: str = load_text(0)

    async def get_suggestion(self, value: str) -> str | None:
        return self.current_text


class ClacktileApp(App):
    CSS_PATH = "style/layers.tcss"
    TITLE = "Clacktile"

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Center():
                yield TextArea(id="text")
            with Center():
                yield TypingArea(
                    placeholder="Start typing",
                    id="input",
                    suggester=StaticSuggester(),
                )

    def on_text_area_text_changed(self, message: TextArea.TextChanged) -> None:
        self.query_one("#input", expect_type=TypingArea).clear()


if __name__ == "__main__":
    app = ClacktileApp()
    app.run()
