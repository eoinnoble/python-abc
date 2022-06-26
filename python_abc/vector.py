import ast
import math
from typing import Optional

# https://en.wikipedia.org/wiki/ABC_Software_Metric
# https://web.archive.org/web/20210606115110/https://www.softwarerenovation.com/ABCMetric.pdf


class Vector:
    __slots__ = ("assignment", "branch", "condition", "lineno", "node")

    def __init__(
        self,
        assignment: int,
        branch: int,
        condition: int,
        lineno: int = 0,  # files start on line 1, so this is essentially a null default
        node: Optional[ast.AST] = None,
    ):
        self.assignment = assignment
        self.branch = branch
        self.condition = condition
        self.lineno = lineno
        self.node = node

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(
            self.assignment + other.assignment,
            self.branch + other.branch,
            self.condition + other.condition,
            self.lineno,
        )

    def __bool__(self) -> bool:
        return self.assignment > 0 or self.branch > 0 or self.condition > 0

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
                    (
                        self.assignment * self.assignment,
                        self.branch * self.branch,
                        self.condition * self.condition,
                    )
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
