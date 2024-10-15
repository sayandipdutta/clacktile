from __future__ import annotations

from typing import override

from textual.app import App, ComposeResult
from textual.containers import Center, Container

from clacktile.common import Status
from clacktile.counter import TimeCountdown
from clacktile.input import TypingArea
from clacktile.static import StaticText
from clacktile.ui_wrapper import wrap_body


class ClacktileApp(App[str]):
    CSS_PATH = "style/layers.tcss"
    TITLE = "Clacktile"
    BINDINGS = [
        ("ctrl+l", "next_static_text()", "Next"),
        ("ctrl+r", "reset()", "Reset"),
        ("ctrl+s", "screenshot()", "Screenshot"),
    ]

    @wrap_body(header=True, footer=True)
    @override
    def compose(self) -> ComposeResult:
        with Container(id="body"):
            with Center():
                yield StaticText(id="text")
            with Container(id="counter"):
                yield TimeCountdown(id="timer", start=10)
            with Center():
                yield TypingArea(id="input")

    def action_next_static_text(self) -> None:
        self.query_one("#text", expect_type=StaticText).next()

    def action_reset(self) -> None:
        _ = self.query_one("#input", expect_type=TypingArea).reset()
        _ = self.query_one("#timer", expect_type=TimeCountdown).reset()

    @override
    def action_screenshot(
        self, filename: str | None = None, path: str | None = None
    ) -> None:
        try:
            saved_filename = super().save_screenshot(filename, path)
        except Exception:
            self.notify("Screenshot could not be saved!", severity="warning")
        else:
            self.notify(f"Screenshot saved in {saved_filename}")

    def on_typing_area_status_changed(self, message: TypingArea.StatusChanged):
        countdown = self.query_one("#timer", expect_type=TimeCountdown)
        match message.status:
            case Status.STARTED:
                countdown.timer.resume()
            case Status.NOT_STARTED:
                countdown.reset()
            case _:
                pass

    def on_counter_status_changed(self, status: TimeCountdown.StatusChanged):
        typing_area = self.query_one("#input", expect_type=TypingArea)
        if status.status is Status.ENDED:
            typing_area.typing_status = status.status

    def on_static_text_changed(self, message: StaticText.Changed):
        _ = self.action_reset()
        del message


if __name__ == "__main__":
    app = ClacktileApp()
    _ = app.run()
