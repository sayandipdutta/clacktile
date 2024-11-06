from contextlib import suppress
from itertools import zip_longest
from statistics import StatisticsError
from typing import cast

from iterdot import Iter
from rich.text import Text


def calculate_accuracy(source: str, typed: str) -> float:
    """Calculate typing accuracy by comparing typed text against source text.

    Splits both strings into words and compares them word by word.
    Returns the mean accuracy (percentage of correctly typed words).

    Args:
        source: The original text to type
        typed: The text that was actually typed

    Returns:
        float: Accuracy as a decimal between 0 and 1, or 0 if calculation fails

    Raises:
        AssertionError: If source string is empty
    """
    with suppress(StatisticsError):
        return (
            Iter(typed.split())
            .zip_with(source.split())
            .starmap(lambda t, s: t == s)
            .stats.mean()
        )
    return 0


def live_feedback(source: str, typed: str) -> Text:
    if not typed:
        return Text(source)

    zipped = zip_longest(source.split(), typed.split())
    return Text.from_markup(
        Iter(zipped)
        .starmap(
            lambda s, t: cast(str, s)
            if ((t is None) or (s == t))
            else f"[red]{s}[/red]"
        )
        .feed_into(" ".join)
    )
