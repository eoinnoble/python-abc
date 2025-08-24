import ast

import pytest

from python_abc import vector


def test_adding_vectors_together():
    empty = vector.empty(ast.AST(), lineno=1)
    assignment = vector.assignment(ast.AST(), lineno=2)

    combined = empty + assignment

    assert combined.assignment == 1
    assert combined.branch == 0
    assert combined.condition == 0
    assert combined.lineno == 1
    assert combined.node is None


@pytest.mark.parametrize(
    "vector_type,as_boolean,as_string,as_notation,magnitude",
    [
        pytest.param(
            vector.empty(ast.AST()),
            False,
            "<0, 0, 0>",
            "",
            "<0, 0, 0> (0.0)",
            id="Empty",
        ),
        pytest.param(
            vector.assignment(ast.AST(), lineno=1),
            True,
            "<1, 0, 0>",
            "a",
            "<1, 0, 0> (1.0)",
            id="Assignment",
        ),
        pytest.param(
            vector.branch(ast.AST(), lineno=1),
            True,
            "<0, 1, 0>",
            "b",
            "<0, 1, 0> (1.0)",
            id="Branch",
        ),
        pytest.param(
            vector.condition(ast.AST(), lineno=1),
            True,
            "<0, 0, 1>",
            "c",
            "<0, 0, 1> (1.0)",
            id="Condition",
        ),
    ],
)
def test_base_vectors(
    vector_type: vector.Vector,
    as_boolean: bool,
    as_string: str,
    as_notation: str,
    magnitude: str,
):
    assert bool(vector_type) is as_boolean
    assert str(vector_type) == as_string
    assert vector_type.as_notation == as_notation
    assert vector_type.magnitude == magnitude
