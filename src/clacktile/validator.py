from contextlib import suppress
from operator import eq
from statistics import StatisticsError
from typing import cast

from iterdot import Iter


def is_equal(a: object, b: object) -> bool:
    return cast(bool, eq(a, b))


def calculate_accuracy(source: str, typed: str) -> float:
    assert source.split(), "Source must not be empty"
    with suppress(StatisticsError):
        return (
            Iter(typed.split())
            .zip_with(source.split())
            .starmap(is_equal)
            .stats.mean()
        )  # fmt: skip
    return 0
