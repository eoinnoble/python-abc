import pytest

from tests.helpers import assert_source_returns_expected


BRANCH_CASES = [
    pytest.param('print("hello world")', 'b | print("hello world")', id="Call"),
    pytest.param("await noop()", "b | await noop()", id="Await"),
    pytest.param("Noop()", "b | Noop()", id="Class instantiation"),
]


@pytest.mark.parametrize("source,expected", BRANCH_CASES)
def test_branch(capsys: pytest.CaptureFixture, source: str, expected: str):
    assert_source_returns_expected(capsys, source, expected)
