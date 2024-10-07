from __future__ import annotations

from typing import override

from textual.app import App, ComposeResult
from textual.containers import Center, Container
from textual.widgets import TextArea

from clacktile.static import StaticText
from clacktile.ui_wrapper import wrap_body


class ClacktileApp(App[str]):
    CSS_PATH = "style/layers.tcss"
    TITLE = "Clacktile"
    BINDINGS = [
        ("ctrl+l", "next_static_text()", "Next"),
        ("ctrl+r", "reset_text()", "Reset"),
        ("ctrl+s", "screenshot", "Screenshot"),
    ]

    @wrap_body(header=True, footer=True)
    @override
    def compose(self) -> ComposeResult:
        with Container():
            with Center():
                yield StaticText(id="text")
            with Center():
                yield TextArea(show_line_numbers=False, id="input")

    def action_next_static_text(self) -> None:
        self.action_reset_text()
        self.query_one("#text", expect_type=StaticText).goto_text()

    def action_reset_text(self) -> None:
        _ = self.query_one("#input", expect_type=TextArea).clear()

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


if __name__ == "__main__":
    app = ClacktileApp()
    _ = app.run()
