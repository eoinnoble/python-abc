import pytest

from tests import assert_source_returns_expected


CONDITION_CASES = [
    # BoolOp
    ("True and False", "cc | True and False"),
    # BoolOp with implicit conditionals
    ("a and b", "cc | a and b"),
    # Test compare
    ("a > b", "c | a > b"),
    # Try/except/finally
    (
        """\
        try:
            a / b
        except ZeroDivisionError:
            pass
        finally:
            pass
        """,
        """\
          | try:
          |     a / b
        c | except ZeroDivisionError:
          |     pass
          | finally:
          |     pass
        """,
    ),
    # Try/except/else
    (
        """\
        try:
            a / b
        except ZeroDivisionError:
            pass
        else:
            pass
        """,
        """\
          | try:
          |     a / b
        c | except ZeroDivisionError:
          |     pass
        c | else:
          |     pass
        """,
    ),
    # If
    ("if True: pass", " | if True: pass"),
    # If with implicit boolean check
    ("if a: pass", "c | if a: pass"),
    # If/else
    (
        """\
        if True:
            pass
        else:
            pass
        """,
        """\
          | if True:
          |     pass
        c | else:
          |     pass
        """,
    ),
    # If/elif/else
    (
        """\
        if True:
            pass
        elif True:
            pass
        else:
            pass
        """,
        """\
          | if True:
          |     pass
        c | elif True:
          |     pass
        c | else:
          |     pass
        """,
    ),
    # For/else
    (
        """\
        for letter in "hello":
            pass
        else:
            pass
        """,
        """\
          | for letter in "hello":
          |     pass
        c | else:
          |     pass
        """,
    ),
    # While/else
    (
        """\
        while True:
            pass
        else:
            pass
        """,
        """\
          | while True:
          |     pass
        c | else:
          |     pass
        """,
    ),
    # Assertion with explicit conditional
    ("assert a > b", "c | assert a > b"),
    # Assertion with tacit conditional
    ("assert a", "c | assert a"),
]


@pytest.mark.parametrize("source,expected", CONDITION_CASES)
def test_condition(capsys, source, expected):
    assert_source_returns_expected(capsys, source, expected) is True
