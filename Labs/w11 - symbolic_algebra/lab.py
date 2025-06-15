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

Operand = Union["Expr", int, float, str]

EvalMapping = dict[str, int | float]


class SymbolicEvaluationError(Exception):
    """
    an expression indicating that something has gone wrong when
    evaluating a symbolic algebra expression.
    """

    pass


# derivatives
# def deriv(self, var: str) -> str:


# base cases
# if an Expr is a Num, then the derivative is zero
# if an Expr is a Var, if the value of Var is var, then the derivative is one,
# otherwise zero.
# non-base cases
# return _apply_operator(self.deriv(self.left), self.deriv(self.right))


class Expr:
    """
    base class for symbolic expressions.

    """

    precedence: int

    def evaluate(self, mapping: EvalMapping) -> int | float:
        raise NotImplementedError

    def deriv(self, var: str) -> "Expr":
        raise NotImplementedError

    def __add__(self, other: Operand) -> "Add":
        return Add(self, other)

    def __radd__(self, other: Operand) -> "Add":
        """
        called in expressions such as 2 + Var('x'), in which the first object's
        __add__ does not know how to add an arbitrary object so the second object's
        __radd__ method is called.
        """

        return Add(other, self)

    def __sub__(self, other: Operand) -> "Sub":
        return Sub(self, other)

    def __rsub__(self, other: Operand) -> "Sub":
        """
        called in expressions such as 2 - Var('x'), in which the first object's
        __sub__ does not know how to subtract an arbitrary object so the second object's
        __rsub__ method is called.
        """

        return Sub(other, self)

    def __mul__(self, other: Operand) -> "Mul":
        return Mul(self, other)

    def __rmul__(self, other: Operand) -> "Mul":
        """
        called in expressions such as 2 * Var('x'), in which the first object's
        __mul__ does not know how to multiply by an arbitrary object so the second object's
        __rmul__ method is called.
        """

        return Mul(other, self)

    def __truediv__(self, other: Operand) -> "Div":
        return Div(self, other)

    def __rtruediv__(self, other: Operand) -> "Div":
        """
        called in expressions such as 2 / Var('x'), in which the first object's
        __div__ does not know how to divide by an arbitrary object so the second object's
        __rdiv__ method is called.
        """

        return Div(other, self)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Expr) and str(self) == str(other)


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
        return f"{self.__class__.__name__}('{self.name}')"

    def evaluate(self, mapping: EvalMapping) -> int | float:
        try:
            return mapping[self.name]
        except KeyError:
            raise SymbolicEvaluationError(
                f"Variable '{self.name}' not found in mapping"
            )

    def deriv(self, var: str) -> "Num":
        if self.name == var:
            return Num(1)
        return Num(0)


class Num(Expr):
    """
    represents numbers within symbolic expressions
    """

    precedence = 0

    def __init__(self, n: int | float):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self) -> str:
        return str(self.n)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.n})"

    def evaluate(self, mapping: EvalMapping) -> int | float:
        return self.n

    def deriv(self, var: str) -> "Num":
        return Num(0)


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
            elif self.operator in ["-", "/"] and self.same_precedence_than(right):
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

    def evaluate(self, mapping: EvalMapping) -> int | float:
        return self._apply_operator(
            self.left.evaluate(mapping), self.right.evaluate(mapping)
        )

    def _apply_operator(self, left: int | float, right: int | float) -> int | float:
        raise NotImplementedError

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"


class Add(BinOp):
    operator = "+"
    precedence = 1

    def _apply_operator(self, left: int | float, right: int | float) -> int | float:
        return left + right

    def deriv(self, var: str) -> "Add":
        return Add(self.left.deriv(var), self.right.deriv(var))


class Sub(BinOp):
    operator = "-"
    precedence = 1

    def _apply_operator(self, left: int | float, right: int | float) -> int | float:
        return left - right

    def deriv(self, var: str) -> "Sub":
        return Sub(self.left.deriv(var), self.right.deriv(var))


class Mul(BinOp):
    operator = "*"
    precedence = 2

    def _apply_operator(self, left: int | float, right: int | float) -> int | float:
        return left * right

    def deriv(self, var: str) -> "Add":
        return Add(
            Mul(self.left, self.right.deriv(var)), Mul(self.right, self.left.deriv(var))
        )


class Div(BinOp):
    operator = "/"
    precedence = 2

    def _apply_operator(self, left: int | float, right: int | float) -> int | float:
        return left / right

    def deriv(self, var: str) -> "Div":
        return Div(
            Sub(
                Mul(self.right, self.left.deriv(var)),
                Mul(self.left, self.right.deriv(var)),
            ),
            Mul(self.right, self.right),
        )


if __name__ == "__main__":
    x = Var("x")
    y = Var("y")

    e1 = x + y + 5 * x + 7
    e2 = x - y - 5 * x + 7
    e3 = x * y
    e4 = x / y

    print(e1.deriv("x"))
    print(e2.deriv("x"))
    print(e3.deriv("x"))
    print(e4.deriv("x"))

    print(repr(e4.deriv("x")))
