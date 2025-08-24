import ast
from textwrap import dedent

import pytest

from python_abc import calculate


def assert_source_returns_expected(
    capsys: pytest.CaptureFixture, input: str, expected: str
) -> None:
    input = dedent(input.rstrip())
    expected = "\n".join(line.strip() for line in expected.split("\n")).rstrip()

    calculate.calculate_abc(input, verbose=True)

    captured = capsys.readouterr()
    output = "\n".join(line.strip() for line in captured.out.split("\n")).rstrip()

    for output_line, expected_line in zip(
        output.split("\n"), expected.split("\n"), strict=True
    ):
        if output_line == expected_line:
            continue

        assert output_line == expected_line, ast.dump(ast.parse(input), indent=4)
