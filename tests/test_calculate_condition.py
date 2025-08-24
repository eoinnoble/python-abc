import pytest

from tests.helpers import assert_source_returns_expected


CONDITION_CASES = [
    pytest.param("True and False", "cc | True and False", id="BoolOp"),
    pytest.param("a and b", "cc | a and b", id="BoolOp with implicit conditionals"),
    pytest.param("a > b", "c | a > b", id="Comparison"),
    pytest.param(
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
        id="Try/except/finally",
    ),
    pytest.param(
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
        id="Try/except/else",
    ),
    pytest.param("if True: pass", " | if True: pass", id="If"),
    pytest.param("if a: pass", "c | if a: pass", id="If with implicit boolean check"),
    pytest.param(
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
        id="If/else",
    ),
    pytest.param(
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
        id="If/elif/else",
    ),
    pytest.param(
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
        id="For/else",
    ),
    pytest.param(
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
        id="While/else",
    ),
    pytest.param(
        "assert a > b", "c | assert a > b", id="Assertion with explicit conditional"
    ),
    pytest.param("assert a", "c | assert a", id="Assertion with tacit conditional"),
]


@pytest.mark.parametrize("source,expected", CONDITION_CASES)
def test_condition(capsys: pytest.CaptureFixture, source: str, expected: str):
    assert_source_returns_expected(capsys, source, expected)
