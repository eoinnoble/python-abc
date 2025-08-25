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
    pytest.param(
        """\
        match x:
            case [x] if x > 0:
                ...
        """,
        """\
            | match x:
        acc |     case [x] if x > 0:
            |         ...
        """,
        id="ast.match_case",
    ),
    pytest.param(
        """\
        match x:
            case "Relevant":
                ...
        """,
        """\
          | match x:
        c |     case "Relevant":
          |         ...
        """,
        id="ast.MatchValue",
    ),
    pytest.param(
        """\
        match x:
            case None:
                ...
        """,
        """\
          | match x:
        c |     case None:
          |         ...
        """,
        id="ast.MatchSingleton",
    ),
    pytest.param(
        """\
        match x:
            case [1, 2]:
                ...
        """,
        """\
          | match x:
        c |     case [1, 2]:
          |         ...
        """,
        id="ast.MatchSequence",
    ),
    pytest.param(
        """\
        match x:
            case [1, 2, *rest]:
                ...
            case [*_]:
                ...
        """,
        """\
           | match x:
        ac |     case [1, 2, *rest]:
           |         ...
        c  |     case [*_]:
           |         ...
        """,
        id="ast.MatchStar",
    ),
    pytest.param(
        """\
        match x:
            case [1, 2]:
                ...
        """,
        """\
          | match x:
        c |     case [1, 2]:
          |         ...
        """,
        id="ast.MatchSequence",
    ),
    pytest.param(
        """\
        match x:
            case {1: _, 2: _}:
                ...
            case {**rest}:
                ...
        """,
        """\
           | match x:
        c  |     case {1: _, 2: _}:
           |         ...
        ac |     case {**rest}:
           |         ...
        """,
        id="ast.MatchMapping",
    ),
    pytest.param(
        """\
        match x:
            case Point2D(0, 0):
                ...
            case Point3D(x=0, y=0, z=0):
                ...
        """,
        """\
          | match x:
        c |     case Point2D(0, 0):
          |         ...
        c |     case Point3D(x=0, y=0, z=0):
          |         ...
        """,
        id="ast.MatchClass",
    ),
    pytest.param(
        """\
        match x:
            case [x] as y:
                ...
            case _:
                ...
        """,
        """\
            | match x:
        aac |     case [x] as y:
            |         ...
        c   |     case _:
            |         ...
        """,
        id="ast.MatchAs",
    ),
    pytest.param(
        """\
        match x:
            case [x] | (y):
                ...
        """,
        """\
            | match x:
        aac |     case [x] | (y):
            |         ...
        """,
        id="ast.MatchOr",
    ),
]


@pytest.mark.parametrize("source,expected", CONDITION_CASES)
def test_condition(capsys: pytest.CaptureFixture, source: str, expected: str):
    assert_source_returns_expected(capsys, source, expected)
