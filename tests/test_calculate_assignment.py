import pytest

from tests.helpers import assert_source_returns_expected


ASSIGNMENT_CASES = [
    # Assignment
    ('e = "hello"', 'a | e = "hello"'),
    # Augmented assignment
    ('e += "world"', 'a | e += "world"'),
    # Assignment with type annotation
    ("(a): int = 1", "a | (a): int = 1"),
    # Assignment by destructuring
    ("a, b, c = d", "aaa | a, b, c = d"),
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
def test_assignment(capsys, source, expected):
    assert_source_returns_expected(capsys, source, expected) is True
