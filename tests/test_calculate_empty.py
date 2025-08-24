import pytest

from tests.helpers import assert_source_returns_expected


EMPTY_CASES = [
    pytest.param(
        """\
        def hello():
            pass
        """,
        """\
          | def hello():
          |     pass
        """,
        id="Function definition",
    ),
    pytest.param(
        """\
        async def hello():
            pass
        """,
        """\
          | async def hello():
          |     pass
        """,
        id="Async function definition",
    ),
    pytest.param(
        """\
        class Hello():
            pass
        """,
        """\
          | class Hello():
          |     pass
        """,
        id="Class definition",
    ),
    pytest.param("[x for x in y]", " | [x for x in y]", id="Comprehension"),
    pytest.param("lambda x: x", " | lambda x: x", id="Lambda"),
]


@pytest.mark.parametrize("source,expected", EMPTY_CASES)
def test_empty(capsys: pytest.CaptureFixture, source: str, expected: str):
    assert_source_returns_expected(capsys, source, expected)
