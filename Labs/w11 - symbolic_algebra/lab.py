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


class Expr:
    """
    base class for symbolic expressions.

    """

    precedence: int

    @staticmethod
    def make_expression(sym: str) -> "Expr":
        tokens = Expr.tokenize(sym)

        return Expr.parse(tokens)

    @staticmethod
    def tokenize(s: str) -> list[str]:
        # traverse sym_str one char at a time
        # if blank space, do nothing
        # if a number, then keep going till the end of the number and save as one token
        # if parentheses or operators, add single token.

        tokens: list[str] = []
        i = 0

        while i < len(s):
            c = s[i]
            if c.isspace():
                i += 1
                continue
            if c in ["(", ")"] or c in ["+", "*", "/"]:
                tokens.append(c)
                i += 1
                continue
            if c == "-":
                if s[i + 1].isdigit() or s[i + 1] == ".":
                    i += 1
                    num: list[str] = ["-"]
                    while i < len(s) and (s[i].isdigit() or s[i] == "."):
                        num.append(s[i])
                        i += 1

                    tokens.append("".join(num))
                    continue
                else:
                    tokens.append(c)
                    i += 1
                    continue
            if c.isdigit() or c == ".":
                num: list[str] = []
                while i < len(s) and (s[i].isdigit() or s[i] == "."):
                    num.append(s[i])
                    i += 1
                tokens.append("".join(num))
                continue
            if c.isalpha():
                tokens.append(c)
                i += 1
                continue
            raise ValueError(f"Unexpected character in input: {c}")

        return tokens

    # @staticmethod
    # def tokenize(sym_str: str) -> list[str]:
    #     tokens: list[str] = []
    #     i = 0
    #     while i < len(sym_str):
    #         c = sym_str[i]
    #         if c.isspace():
    #             i += 1
    #         elif c in "()+*/":
    #             tokens.append(c)
    #             i += 1
    #         elif (
    #             c == "-"
    #             and (i + 1 < len(sym_str))
    #             and (sym_str[i + 1].isdigit() or sym_str[i + 1] == ".")
    #         ):
    #             # Start of a negative number
    #             num = c
    #             i += 1
    #             while i < len(sym_str) and (sym_str[i].isdigit() or sym_str[i] == "."):
    #                 num += sym_str[i]
    #                 i += 1
    #             tokens.append(num)
    #         elif c.isdigit() or c == ".":
    #             # Start of a non-negative number
    #             num = c
    #             i += 1
    #             while i < len(sym_str) and (sym_str[i].isdigit() or sym_str[i] == "."):
    #                 num += sym_str[i]
    #                 i += 1
    #             tokens.append(num)
    #         elif c.isalpha():
    #             tokens.append(c)
    #             i += 1
    #         else:
    #             raise ValueError(f"Unexpected character in input: {c}")
    #     return tokens

    @staticmethod
    def parse(tokens: list[str]) -> "Expr":

        def parse_expression(index: int) -> tuple["Expr", int]:
            token = tokens[index]

            operators = {"+": Add, "-": Sub, "*": Mul, "/": Div}

            if token == "(":
                e1, ni = parse_expression(index + 1)
                while tokens[ni] != ")":
                    op = tokens[ni]
                    e2, ni = parse_expression(ni + 1)
                    current = operators[op](e1, e2)
                    e1 = current
                return (current, ni + 1)

            try:
                number_token = float(token)
                return (Num(number_token), index + 1)
            except ValueError:
                return (Var(token), index + 1)

        parsed_expression, next_index = parse_expression(0)

        return parsed_expression

    def evaluate(self, mapping: EvalMapping) -> int | float:
        raise NotImplementedError

    def deriv(self, var: str) -> "Expr":
        raise NotImplementedError

    def simplify(self) -> "Expr":
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
        return isinstance(other, self.__class__) and str(self) == str(other)


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

    def simplify(self) -> "Expr":
        return self


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

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Num) and self.n == other.n

    def evaluate(self, mapping: EvalMapping) -> int | float:
        return self.n

    def deriv(self, var: str) -> "Num":
        return Num(0)

    def simplify(self) -> "Expr":
        return self


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

    def simplify(self) -> "Expr":
        left = self.left.simplify()
        right = self.right.simplify()

        if left == Num(0):
            return right
        if right == Num(0):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(self._apply_operator(left.n, right.n))

        return Add(left, right)


class Sub(BinOp):
    operator = "-"
    precedence = 1

    def _apply_operator(self, left: int | float, right: int | float) -> int | float:
        return left - right

    def deriv(self, var: str) -> "Sub":
        return Sub(self.left.deriv(var), self.right.deriv(var))

    def simplify(self) -> "Expr":
        left = self.left.simplify()
        right = self.right.simplify()

        if right == Num(0):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(self._apply_operator(left.n, right.n))

        return Sub(left, right)


class Mul(BinOp):
    operator = "*"
    precedence = 2

    def _apply_operator(self, left: int | float, right: int | float) -> int | float:
        return left * right

    def deriv(self, var: str) -> "Add":
        return Add(
            Mul(self.left, self.right.deriv(var)), Mul(self.right, self.left.deriv(var))
        )

    def simplify(self) -> "Expr":
        left = self.left.simplify()
        right = self.right.simplify()

        if left == Num(0) or right == Num(0):
            return Num(0)
        if left == Num(1):
            return right
        if right == Num(1):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(self._apply_operator(left.n, right.n))

        return Mul(left, right)


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

    def simplify(self) -> "Expr":
        left = self.left.simplify()
        right = self.right.simplify()

        if left == Num(0):
            return Num(0)
        if right == Num(1):
            return left
        if isinstance(left, Num) and isinstance(right, Num):
            return Num(self._apply_operator(left.n, right.n))

        return Div(left, right)


def make_expression(sym_str):
    tokens = Expr.tokenize(sym_str)
    parsed = Expr.parse(tokens)
    return parsed


if __name__ == "__main__":
    x = Var("x")
    y = Var("y")

    tokens = Expr.tokenize("20")
    # parsed = Expr.parse(tokens)

    print(tokens)
    # print(repr(parsed))
