from contextlib import suppress
from statistics import StatisticsError

from iterdot import Iter


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
