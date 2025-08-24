import pytest

from tests.helpers import assert_source_returns_expected


ASSIGNMENT_CASES = [
    pytest.param('e = "hello"', 'a | e = "hello"', id="Assignment"),
    pytest.param('e += "world"', 'a | e += "world"', id="Augmented assignment"),
    pytest.param(
        "(a): int = 1", "a | (a): int = 1", id="Assignment with type annotation"
    ),
    pytest.param("a, b, c = d", "aaa | a, b, c = d", id="Assignment by destructuring"),
    pytest.param(
        "if a := {'found': True}: pass",
        "ac | if a := {'found': True}: pass",
        id="Walrus operator assignment, implicit else",
    ),
    pytest.param(
        """\
        if a := {'found': True}:
            pass
        else:
            pass
        """,
        """\
        ac | if a := {'found': True}:
           |     pass
        c  | else:
           |     pass
        """,
        id="Walrus operator assignment, if/else",
    ),
    pytest.param(
        """\
        if a := {'found': True}:
            pass
        elif b := {'also_found': True}:
            pass
        else:
            pass
        """,
        """\
        ac  | if a := {'found': True}:
            |     pass
        acc | elif b := {'also_found': True}:
            |     pass
        c   | else:
            |     pass
        """,
        id="Walrus operator assignment, if/elif/else",
    ),
]


@pytest.mark.parametrize("source,expected", ASSIGNMENT_CASES)
def test_assignment(capsys: pytest.CaptureFixture, source: str, expected: str):
    assert_source_returns_expected(capsys, source, expected)
