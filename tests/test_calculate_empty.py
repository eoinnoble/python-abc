import pytest

from tests import assert_source_returns_expected


EMPTY_CASES = [
    # Function definition
    (
        """\
        def hello():
            pass
        """,
        """\
          | def hello():
          |     pass
        """,
    ),
    # Async function definition
    (
        """\
        async def hello():
            pass
        """,
        """\
          | async def hello():
          |     pass
        """,
    ),
    # Class definition
    (
        """\
        class Hello():
            pass
        """,
        """\
          | class Hello():
          |     pass
        """,
    ),
    # Comprehension
    ("[x for x in y]", " | [x for x in y]"),
    # Lambda
    ("lambda x: x", " | lambda x: x"),
]


@pytest.mark.parametrize("source,expected", EMPTY_CASES)
def test_empty(capsys, source, expected):
    assert_source_returns_expected(capsys, source, expected) is True
