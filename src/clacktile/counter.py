from __future__ import annotations

from dataclasses import dataclass

from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from clacktile.common import Status


class Counter(Static):
    @dataclass
    class StatusChanged(Message):
        status: Status


class TimeCountdown(Counter):
    time = reactive(0, init=False)

    def __init__(self, *, start: int, id: str | None = None) -> None:
        renderable = construct_renderable(start)
        super().__init__(renderable, id=id)
        self.timer = self.set_interval(1, self.countdown, pause=True)
        self.start = start
        self.time = start

    def watch_time(self, time: int):
        if time == 0:
            self.timer.pause()
            _ = self.post_message(self.StatusChanged(Status.ENDED))
        elif time <= 5:
            self.styles.animate("opacity", value=0.2, final_value=1.0, duration=0.9)
            self.styles.animate("color", value="red", duration=4.0)

    def countdown(self):
        self.time -= 1
        updated_time = construct_renderable(self.time)
        self.update(updated_time)

    def reset(self):
        self.timer.reset()
        self.timer.pause()
        _ = self.post_message(self.StatusChanged(Status.NOT_STARTED))
        self.time = self.start
        self.renderable = construct_renderable(self.start)
        self.styles.reset()

    def elapsed_time(self, handle_zero: bool = True) -> int:
        elapsed = self.start - self.time
        if handle_zero and not elapsed:
            elapsed += 1
        return elapsed


def construct_renderable(start: int) -> str:
    minutes, seconds = divmod(start, 60)
    return f"{minutes:02d}:{seconds:02d}"
