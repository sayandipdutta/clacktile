from contextlib import suppress
from itertools import zip_longest
from statistics import StatisticsError

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


FAILURE = "[red]{}[/red]".format
MATCHES = "[yellow]{}[/yellow]".format
SUCCESS = "[green]{}[/green]".format


def live_feedback(source: str, typed: str) -> Text:
    if not typed:
        return Text(source)

    def map_color(s: str, t: str | None) -> str:
        if t is None:
            return s
        elif s == t:
            return SUCCESS(s)
        elif s.startswith(t):
            return MATCHES(t) + s.removeprefix(t)
        else:
            return FAILURE(s)

    zipped = zip_longest(source.split(), typed.split())
    return Text.from_markup(
        Iter(zipped)
        .starmap(map_color)
        .feed_into(" ".join)
    )  # fmt: skip


def live_speed(typed: str, time: int) -> float:
    return len(typed.split()) / (time / 60)


if __name__ == "__main__":
    from rich import print

    source = "I must not fear"
    typed = "I musr not few"

    for i, char in enumerate(typed, start=1):
        print(live_feedback(source, typed[:i]))
