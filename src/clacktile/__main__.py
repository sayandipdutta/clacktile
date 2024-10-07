from __future__ import annotations

from pathlib import Path
from typing import Final, override

from textual.app import App, ComposeResult, RenderResult
from textual.containers import Center, Container
from textual.message import Message
from textual.reactive import reactive
from textual.suggester import Suggester
from textual.widgets import Footer, Header, Input, Static, TextArea

SAVED_TEXT_PATH: Final[Path] = Path(__file__).parent / "saved"


def load_text(index: int) -> str:
    files = list(SAVED_TEXT_PATH.glob("*.txt"))
    if not files:
        return "No files available"
    index %= len(files)
    return files[index].read_text()


class StaticText(Static, can_focus=True):
    BINDINGS = [
        ("left,h", "goto_text(-1)", "Previous"),
        ("right,l", "goto_text(1)", "Next"),
    ]

    count = reactive(0)
    text = reactive(load_text(0))

    class TextChanged(Message):
        def __init__(self, text: str) -> None:
            self.text = text
            super().__init__()

    @override
    def render(self) -> RenderResult:
        return self.text

    def action_goto_text(self, amount: int) -> None:
        print("action go to next ########")
        self.count += amount
        self.text = load_text(self.count)
        _ = self.post_message(self.TextChanged(self.text))
        StaticSuggester.current_text = self.text


# class TypingArea(Input):
#     BINDINGS = Input.BINDINGS + [
#         ("ctrl+h", "next_static_text()", "Next"),
#         ("ctrl+l", "prev_static_text()", "Prev"),
#     ]
#
#     class RequestTextChange(Message):
#         def __init__(self, direction: int) -> None:
#             self.direction = direction
#             super().__init__()
#
#     @override
#     def action_cursor_right(self) -> None:
#         self.cursor_position += 1
#
#     def action_next_static_text(self) -> None:
#         _ = self.post_message(self.RequestTextChange(1))
#
#     def action_prev_static_text(self) -> None:
#         _ = self.post_message(self.RequestTextChange(-1))


class TypingArea(TextArea):
    BINDINGS = [
        ("ctrl+l", "next_static_text()", "Next"),
        ("ctrl+h", "prev_static_text()", "Prev"),
    ]

    class RequestTextChange(Message):
        def __init__(self, direction: int) -> None:
            self.direction = direction
            super().__init__()

    def action_next_static_text(self) -> None:
        _ = self.post_message(self.RequestTextChange(1))

    def action_prev_static_text(self) -> None:
        _ = self.post_message(self.RequestTextChange(-1))


class StaticSuggester(Suggester):
    current_text: str = load_text(0)

    @override
    async def get_suggestion(self, value: str) -> str | None:
        return self.current_text


class ClacktileApp(App[str]):
    CSS_PATH = "style/layers.tcss"
    TITLE = "Clacktile"

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            with Center():
                yield StaticText(id="text")
            with Center():
                yield TypingArea(show_line_numbers=False, id="input")
                # yield TypingArea(
                #     placeholder="Start typing",
                #     suggester=StaticSuggester(),
                #     id="input",
                # )
        yield Footer()

    def on_text_area_text_changed(self, message: StaticText.TextChanged) -> None:
        _ = self.query_one("#input", expect_type=TypingArea).clear()

    def on_typing_area_request_text_change(
        self, message: TypingArea.RequestTextChange
    ) -> None:
        print("triggered from typing area")
        self.query_one("#text", expect_type=StaticText).action_goto_text(
            message.direction
        )


if __name__ == "__main__":
    app = ClacktileApp()
    _ = app.run()
