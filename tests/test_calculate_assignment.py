import pytest

from tests import assert_source_returns_expected


ASSIGNMENT_CASES = [
    # Assignment
    ('e = "hello"', 'a | e = "hello"'),
    # Augmented assignment
    ('e += "world"', 'a | e += "world"'),
    # Assignment with type annotation
    ("(a): int = 1", "a | (a): int = 1"),
    # Assignment by destructuring
    ("a, b, c = d", "aaa | a, b, c = d"),
]


@pytest.mark.parametrize("source,expected", ASSIGNMENT_CASES)
def test_assignment(capsys, source, expected):
    assert_source_returns_expected(capsys, source, expected) is True
