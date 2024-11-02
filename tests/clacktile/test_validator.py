from math import isclose

import pytest

from clacktile.validator import calculate_accuracy


test_data = (
    (("I must not fear", "I must not fear", 1.0), "Identical"),
    (("I must not fear", "I must not", 1.0), "Accurate but short"),
    (("I must not fear", "I must not fear fear", 1.0), "Accurate but long"),
    (("I must not fear", "I must yes fear", 3 / 4), "Semi-Accurate but eqlength"),
    (("I must not fear", "You must not", 2 / 3), "Semi-Accurate but short"),
    (("I must not fear", "I must yes fear Fear", 3 / 4), "Semi-Accurate but long"),
    (("I must not fear", "If they ever tell", 0.0), "Wrong but eqlength"),
    (("I must not fear", "If they ever tell my", 0.0), "Wrong but long"),
    (("I must not fear", "If they ever", 0.0), "Wrong but short"),
    (("I must not fear", "", 0.0), "Nothing typed"),
    (("", "", "Source must not be empty"), "Source Empty"),
    (("", "I", "Source must not be empty"), "Source Empty"),
)

parameters, ids = zip(*test_data)


@pytest.mark.parametrize("source,typed,expected", parameters, ids=ids)
def test_identical(source: str, typed: str, expected: float | str) -> None:
    if isinstance(expected, float):
        assert isclose(
            (found := calculate_accuracy(source, typed)), expected
        ), f"Accuracy should be {expected}, found {found}"
    elif isinstance(expected, str):
        with pytest.raises(AssertionError, match=expected):
            _ = calculate_accuracy(source, expected)
