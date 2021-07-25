from textwrap import dedent

import pytest

import calculate


def assert_source_returns_expected(
    capsys: pytest.CaptureFixture, input: str, expected: str
) -> None:
    input = dedent(input.rstrip())
    expected = "\n".join(line.strip() for line in expected.split("\n")).rstrip()

    calculate.calculate_abc(input, verbose=True)
    captured = capsys.readouterr()

    output = "\n".join(line.strip() for line in captured.out.split("\n")).rstrip()

    assert output == expected, (output, expected)
