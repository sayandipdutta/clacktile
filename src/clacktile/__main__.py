from __future__ import annotations

from typing import override

from textual.app import App, ComposeResult
from textual.containers import Center, Container
from textual.widgets import Static

from clacktile.common import Status
from clacktile.counter import TimeCountdown
from clacktile.input import TypingArea
from clacktile.static import StaticText
from clacktile.ui_wrapper import wrap_body
from clacktile.validator import calculate_accuracy, live_feedback, live_speed


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
            with Center():
                with Container(classes="counter"):
                    yield Static(id="speed")
                    yield Static(id="accuracy")
                    yield TimeCountdown(id="timer", start=10)
            with Center():
                yield TypingArea(id="input")

    def on_mount(self):
        _ = self.query_one("#input").focus()

    def action_next_static_text(self) -> None:
        self.query_one("#text", expect_type=StaticText).next()

    def action_reset(self) -> None:
        _ = self.query_one("#input", expect_type=TypingArea).reset()
        _ = self.query_one("#timer", expect_type=TimeCountdown).reset()
        self.query_one("#speed", expect_type=Static).update()
        self.query_one("#accuracy", expect_type=Static).update()
        (s := self.query_one("#text", expect_type=StaticText)).update(str(s.renderable))

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
                self.query_one("#speed", expect_type=Static).update()
                self.query_one("#accuracy", expect_type=Static).update()
            case Status.ENDED:
                self.update_speed(countdown.start)
                self.update_accuracy()

    def on_typing_area_editing(self, message: TypingArea.Editing):
        source = self.query_one("#text", expect_type=StaticText)
        source.update(live_feedback(str(source.renderable), message.text))
        countdown = self.query_one("#timer", expect_type=TimeCountdown)
        elapsed = (countdown.start - countdown.time) or 1
        self.query_one("#speed", expect_type=Static).update(
            live_speed(message.text, elapsed)
        )

    def on_counter_status_changed(self, status: TimeCountdown.StatusChanged):
        typing_area = self.query_one("#input", expect_type=TypingArea)
        if status.status is Status.ENDED:
            typing_area.typing_status = status.status

    def on_static_text_changed(self, message: StaticText.Changed):
        _ = self.action_reset()
        del message

    def update_speed(self, time_elapsed_sec: int):
        text = self.query_one("#input", expect_type=TypingArea).text
        speed = live_speed(text, time_elapsed_sec)
        self.query_one("#speed", expect_type=Static).update(speed)

    def update_accuracy(self):
        typed = self.query_one("#input", expect_type=TypingArea).text
        static = str(self.query_one("#text", expect_type=StaticText).renderable)
        acc = calculate_accuracy(static, typed)
        self.query_one("#accuracy", expect_type=Static).update(f"{acc:.02%}")


if __name__ == "__main__":
    app = ClacktileApp()
    _ = app.run()
