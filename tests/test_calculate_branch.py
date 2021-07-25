import pytest

from tests import assert_source_returns_expected


BRANCH_CASES = [
    # Call
    ('print("hello world")', 'b | print("hello world")'),
    # Await
    ("await noop()", "b | await noop()"),
    # Class instantiation
    ("Noop()", "b | Noop()"),
]


@pytest.mark.parametrize("source,expected", BRANCH_CASES)
def test_branch(capsys, source, expected):
    assert_source_returns_expected(capsys, source, expected) is True
