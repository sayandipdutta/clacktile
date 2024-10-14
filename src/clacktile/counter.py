from __future__ import annotations

from dataclasses import dataclass

from rich.console import RenderableType
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from clacktile.common import Status


class Counter(Static):
    @dataclass
    class StatusChanged(Message):
        status: Status


class TimeCountdown(Counter):
    time = reactive(1)

    def __init__(
        self, renderable: RenderableType, *, start: int, id: str | None = None
    ) -> None:
        super().__init__(renderable, id=id)
        self.timer = self.set_interval(1, self.update_time, pause=True)
        self.start = start
        self.time = start
        self.init = self.renderable

    def watch_time(self, time: int):
        if time == 0:
            self.timer.pause()
            self.post_message(self.StatusChanged(Status.ENDED))
        elif time == self.start:
            self.timer.pause()
            self.post_message(self.StatusChanged(Status.NOT_STARTED))

    def update_time(self):
        if self.time > 0:
            self.time -= 1
        minutes, seconds = divmod(self.time, 60)
        updated_time = f"{minutes:02d}:{seconds:02d}"
        if 0 < self.time < 5:
            updated_time = f"[blink red]{updated_time}"
        elif self.time == 0:
            updated_time = f"[red]{updated_time}"
        self.update(updated_time)

    def reset(self):
        self.timer.reset()
        self.timer.pause()
        self.time = self.start
        self.renderable = self.init
