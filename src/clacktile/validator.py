from contextlib import suppress
from statistics import StatisticsError

from iterdot import Iter
from iterdot.defaults import Pad
from rich.console import RenderableType
from rich.text import Text


def calculate_accuracy(source: RenderableType, typed: RenderableType) -> float:
    """Calculate typing accuracy by comparing typed text against source text.

    Splits both strings into words and compares them word by word.
    Returns the mean accuracy (percentage of correctly typed words).

    Args:
        source: The original text to type
        typed: The text that was actually typed

    Returns:
        float: Accuracy as a decimal between 0 and 1, or 0 if calculation fails
    """
    with suppress(StatisticsError):
        return (
            Iter(str(typed).split())
            .zip(str(source).split())
            .starmap(lambda t, s: t == s)
            .stats.mean()
        )
    return 0


def calculate_speed(typed: str, time: int) -> float:
    return len(typed.split()) / (time / 60)


def format_accuracy(acc: float) -> str:
    return f"ACCURACY: {acc:.02%}"


FAILURE = "[red]{}[/red]".format
MATCHES = "[yellow]{}[/yellow]".format
SUCCESS = "[green]{}[/green]".format


def live_feedback(source: str, typed: str) -> Text:
    if not typed:
        return Text(source)

    def map_color(s: str | None, t: str | None) -> str:
        assert s is not None
        if t is None:
            return s
        elif s == t:
            return SUCCESS(s)
        elif s.startswith(t):
            return MATCHES(t) + s.removeprefix(t)
        else:
            return FAILURE(s)

    return Text.from_markup(
        Iter(source.split())
        .zip(typed.split(), missing_policy=Pad(None))
        .starmap(map_color)
        .feed_into(" ".join)
    )


def live_speed(typed: str, time: int) -> str:
    speed = calculate_speed(typed, time)
    return f"SPEED: {speed:.02f} WPM"


if __name__ == "__main__":
    from rich import print

    source = "I must not fear"
    typed = "I musr not few"

    Iter(typed).enumerate().map(
        lambda char: live_feedback(source, typed[: char.idx])
    ).foreach(print)
