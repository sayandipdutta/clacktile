from dataclasses import dataclass
from enum import Enum, auto

from textual.widgets import Static


class Status(Enum):
    NOT_STARTED = auto()
    STARTED = auto()
    ENDED = auto()


class Counter(Static):
    @dataclass
    class StatusChanged:
        status: Status
