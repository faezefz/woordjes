"""Leitner spaced-repetition logic.

Each word lives in a box from 1 to 5. A correct answer moves the word
one box up (so it comes back later); a wrong answer sends it back to box 1.
"""

from datetime import date, timedelta

MIN_BOX = 1
MAX_BOX = 5

# How many days to wait before a word in each box is due again.
INTERVAL_DAYS = {1: 0, 2: 1, 3: 3, 4: 7, 5: 14}


def next_box(box: int, correct: bool) -> int:
    """Return the new box after an answer."""
    if not correct:
        return MIN_BOX
    return min(box + 1, MAX_BOX)


def next_due(box: int, today: date) -> date:
    """Return the date a word in `box` should be reviewed again."""
    return today + timedelta(days=INTERVAL_DAYS[box])


def normalize(answer: str) -> str:
    """Make answers comparable: trim spaces and ignore upper/lower case."""
    return " ".join(answer.strip().lower().split())


def is_correct(given: str, expected: str) -> bool:
    """Check an answer. Several correct answers can be separated by ';'."""
    options = [normalize(o) for o in expected.split(";")]
    return normalize(given) in options
