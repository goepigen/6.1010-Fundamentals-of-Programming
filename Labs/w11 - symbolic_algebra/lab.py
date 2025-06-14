"""
6.101 Lab:
Symbolic Algebra
"""

# import doctest # optional import
# import typing # optional import
from typing import Union, assert_never

# import pprint # optional import
# import string # optional import
# import abc # optional import


# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.
class Expr:
    """
    base class for symbolic expressions.

    """

    precedence: int
    pass


class Var(Expr):
    """
    represents variables.
    """

    precedence = 0

    def __init__(self, name: str):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Var('{self.name}')"


class Num(Expr):
    """
    represents numbers within symbolic expressions
    """

    precedence = 0

    def __init__(self, val: int | float):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.val = val

    def __str__(self) -> str:
        return str(self.val)

    def __repr__(self) -> str:
        return f"Num({self.val})"


Operand = Union["Expr", int, float, str]


class BinOp(Expr):
    """
    represents a binary operation.

    spec allows only the two instance variables left and right.
    """

    operator: str

    def __init__(self, left: Operand, right: Operand):

        self.left: "Expr" = self._wrap(left)
        self.right: "Expr" = self._wrap(right)

    def higher_precedence_than(self, other: "Expr") -> bool:
        return self.precedence > other.precedence

    def same_precedence_than(self, other: "Expr") -> bool:
        return self.precedence == other.precedence

    def parenthesize(self, expr: Expr) -> str:
        return f"({str(expr)})"

    def __str__(self) -> str:
        left = self.left
        right = self.right

        if left.precedence > 0 and self.higher_precedence_than(left):
            left = self.parenthesize(left)
        if right.precedence > 0:
            if self.higher_precedence_than(right):
                right = self.parenthesize(right)
            elif (
                self.operator == "-"
                or self.operator == "/"
                and self.same_precedence_than(right)
            ):
                right = self.parenthesize(right)

        return f"{left} {self.operator} {right}"

    @staticmethod
    def _wrap(val: Operand) -> "Expr":
        if isinstance(val, Expr):
            return val
        elif isinstance(val, (int, float)):
            return Num(val)
        elif isinstance(val, str):  # type: ignore[reportUnnecessaryCode]
            return Var(val)
        else:
            assert_never(val)


class Add(BinOp):
    operator = "+"
    precedence = 1


class Sub(BinOp):
    operator = "-"
    precedence = 1


class Mul(BinOp):
    operator = "*"
    precedence = 2


class Div(BinOp):
    operator = "/"
    precedence = 2


if __name__ == "__main__":
    pass
