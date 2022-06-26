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
        (vector.empty(ast.AST()), False, "<0, 0, 0>", "", "<0, 0, 0> (0.0)"),
        (
            vector.assignment(ast.AST(), lineno=1),
            True,
            "<1, 0, 0>",
            "a",
            "<1, 0, 0> (1.0)",
        ),
        (vector.branch(ast.AST(), lineno=1), True, "<0, 1, 0>", "b", "<0, 1, 0> (1.0)"),
        (
            vector.condition(ast.AST(), lineno=1),
            True,
            "<0, 0, 1>",
            "c",
            "<0, 0, 1> (1.0)",
        ),
    ],
)
def test_base_vectors(vector_type, as_boolean, as_string, as_notation, magnitude):
    assert bool(vector_type) is as_boolean
    assert str(vector_type) == as_string
    assert vector_type.as_notation == as_notation
    assert vector_type.magnitude == magnitude
