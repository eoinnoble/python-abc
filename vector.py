import ast
import math
from dataclasses import Field, dataclass, fields
from typing import Annotated, List, Optional

# https://en.wikipedia.org/wiki/ABC_Software_Metric
# https://web.archive.org/web/20210606115110/https://www.softwarerenovation.com/ABCMetric.pdf


@dataclass
class Vector:
    assignment: int
    branch: int
    condition: int
    lineno: int = 0  # files start on line 1, so this is essentially a null default
    node: Optional[ast.AST] = None

    @property
    def metric_fields(self) -> Annotated[List[Field], 3]:
        return [
            field
            for field in fields(self)
            if field.name in ["assignment", "branch", "condition"]
        ]

    def __add__(self, other) -> "Vector":
        if not isinstance(other, type(self)):
            raise TypeError(
                f'unsupported operand type(s) for +: "{type(self)}" and "{type(other)}"'
            )

        assignment, branch, condition = (
            getattr(self, count_type.name) + getattr(other, count_type.name)
            for count_type in self.metric_fields
        )

        return Vector(assignment, branch, condition, self.lineno)

    def __bool__(self) -> bool:
        return any(
            getattr(self, count_type.name) > 0 for count_type in self.metric_fields
        )

    def __str__(self) -> str:
        return f"<{self.assignment}, {self.branch}, {self.condition}>"

    @property
    def as_notation(self) -> str:
        return ("a" * self.assignment) + ("b" * self.branch) + ("c" * self.condition)

    def get_magnitude_value(self) -> float:
        """Fitzpatrick's original paper defines the magnitude for a given vector as

            |ABC| = sqrt((A*A)+(B*B)+(C*C)

        and 'is always rounded to the nearest tenth and is reported using one digit following the
        decimal point'"""
        return round(
            math.sqrt(
                sum(
                    [
                        math.pow(getattr(self, count_type.name), 2)
                        for count_type in self.metric_fields
                    ]
                )
            ),
            1,
        )

    @property
    def magnitude(self) -> str:
        """Fitzpatrick's original paper says that the magnitude value 'should not be presented
        without the accompanying ABC vector.'"""
        return f"{str(self)} ({self.get_magnitude_value()})"


def empty(node_class: ast.AST, lineno=None) -> Vector:
    lineno = lineno if lineno else getattr(node_class, "lineno", 0)
    return Vector(0, 0, 0, lineno, node_class)


def assignment(node_class: ast.AST, lineno=None) -> Vector:
    lineno = lineno if lineno else node_class.lineno
    return Vector(1, 0, 0, lineno, node_class)


def branch(node_class: ast.AST, lineno=None) -> Vector:
    lineno = lineno if lineno else node_class.lineno
    return Vector(0, 1, 0, lineno, node_class)


def condition(node_class: ast.AST, lineno=None) -> Vector:
    lineno = lineno if lineno else node_class.lineno
    return Vector(0, 0, 1, lineno, node_class)
