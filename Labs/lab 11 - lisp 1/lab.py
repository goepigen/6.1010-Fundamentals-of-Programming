"""
6.101 Lab:
LISP Interpreter Part 1
"""

#!/usr/bin/env python3

# import doctest # optional import
from typing import Callable, Any, Union  # optional import
from functools import reduce

# import pprint  # optional import

import sys

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def traverse_number(s: str, i: int, negative: bool = False) -> tuple[int, str]:
    num: list[str] = []
    if negative:
        num.append("-")
        i += 1
    while i < len(s) and (s[i].isdigit() or s[i] == "."):
        num.append(s[i])
        i += 1
    return i, "".join(num)


def traverse_variable(s: str, i: int) -> tuple[int, str]:
    var: list[str] = []
    while i < len(s):
        c = s[i]
        if not c.isspace() and not c == ")" and not c == "(" and not c == ";":
            var.append(c)
            i += 1
        else:
            break
    return i, "".join(var)


def tokenize(s: str) -> list[str]:
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    tokens: list[str] = []
    i = 0
    # traverse the source string starting at position 0
    while i < len(s):
        c = s[i]

        # case 1: space character -> do nothing, move to next character
        if c.isspace() or c == "\n":
            i += 1
            continue
        # case 2: if we encounter parens or an operator (except subtract operator, a special case)
        # add that char to tokens, move on
        if c in ["(", ")"] or c in ["+", "*", "/"]:
            tokens.append(c)
            i += 1
            continue
        # case 3: if we encounter a dash
        # case 3.2: otherwise, the dash is a subtraction operator, which we append to tokens, and
        # then we move on.
        if c == "-":
            # case 3.1 if the next char is a digit or a decimal point then this is a negative sign
            # in this case we keep traversing and saving the digits to a list until we reach a non-digit
            # at which point we append the entire number (with negative sign) to tokens.
            if s[i + 1].isdigit() or s[i + 1] == ".":
                i, num = traverse_number(s, i, False)
                tokens.append(num)
                continue
            # case 3.2: otherwise, the dash is a subtraction operator, which we append to tokens, and
            # then we move on.
            else:
                tokens.append(c)
                i += 1
                continue
        # case 4: if we encounter a digit, then we proceed as in case 3.1 and save the entire number
        # to tokens (without a positive sign in this case).
        if c.isdigit() or c == ".":
            i, num = traverse_number(s, i, False)
            tokens.append(num)
            continue

        # case 6: if we encounter ";" then everything that comes after on the same line is ignored
        # IMPROVE THIS CASE
        if c == ";":
            nl_pos = s[i:].find("\n")
            if nl_pos == -1:
                break
            else:
                i += nl_pos + 1
                continue
        # case 5: if we encounter an alphabetic character, we add it to tokens and move on (the assumption
        # here is that variables are one character long)
        else:
            i, var = traverse_variable(s, i)
            tokens.append(var)
            continue

        # if we reach this point then the character in the source string is not of an accepted type and so
        # the source string is in an incorrect format.
        # raise ValueError(f"Unexpected character in input: {c}")

    return tokens


Parsed = int | float | str | list[int | float | str]


def parse(tokens: list[str]) -> Parsed:
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens

    >>> parse(['2'])
    2
    >>> parse(['x'])
    'x'
    >>> parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')'])
    ['+', 2, ['-', 5, 3], 7, 8]
    """

    def parse_expression(index: int):
        # consider one token at a time
        token = tokens[index]
        # parentheses represent s-expressions
        if token == "(":
            # create a list to represent the s-expression
            s_expr: list[int | float | str] = []
            # if the s-expression is empty, return an empty list
            if tokens[index + 1] == ")":
                return (s_expr, index + 1)
            # otherwise, the s-expression is not empty, so parse it
            # starting at the first token after the open parens, which
            # is a special expression determining what the s-expr means.
            se1, ni = parse_expression(index + 1)
            # add the special expr to the list representing the s-expr
            s_expr.append(se1)
            # then, keep parsing expressions in the s-expr until a closing
            # parens is encountered.
            while tokens[ni] != ")":
                se, ni = parse_expression(ni)
                if se != []:
                    s_expr.append(se)
            # return the s_expr
            return (s_expr, ni + 1)
        # if the token is not an opening parens, then it must be an atomic
        # expression, ie either a number or a symbol.
        # we convert a number to either int or float, and leave symbols as str.
        try:
            return (int(token), index + 1)
        except ValueError:
            try:
                return (float(token), index + 1)
            except ValueError:
                return (token, index + 1)

    parsed_expression, _ = parse_expression(0)

    return parsed_expression


######################
# Built-in Functions #
######################

Number = Union[int, float]


def calc_sub(*args: Any) -> Any:
    if len(args) == 1:
        return -args[0]

    first_num, *rest_nums = args
    return first_num - scheme_builtins["+"](*rest_nums)


def calc_mul(*args: Number) -> Number:
    if not args:
        return 1
    return reduce(lambda acc, x: acc * x, args, 1)


def calc_div(*args: Number) -> Number:
    if not args:
        raise TypeError("division requires at least one argument.")
    if len(args) == 1:
        return 1 / args[0]
    return reduce(lambda acc, x: acc / x, args)


scheme_builtins: dict[str, Callable[..., Number]] = {
    "+": lambda *args: sum(args),
    "-": calc_sub,
    "*": calc_mul,
    "/": calc_div,
}


##############
# Evaluation #
##############


def evaluate(tree: Parsed) -> Callable[..., Any] | int | float:
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    >>> evaluate(3.14)
    3.14
    >>> evaluate(['+', 1, 2])
    3
    >>> evaluate([3.14])
    Traceback (most recent call last):
    ...
    lab.SchemeEvaluationError: 3.14 not callable

    >>> evaluate(['a', 1, 2])
    Traceback (most recent call last):
    ...
    lab.SchemeNameError: Invalid symbol

    >>> evaluate(['+', 3, ['-', 7, 5]])
    5
    """
    # if tree is a string, then it is an operation and we
    # find the associated function in the scheme_builtins dict and return it
    if isinstance(tree, str):
        try:
            return scheme_builtins[tree]
        except KeyError:
            raise SchemeNameError("Invalid symbol")
    # if tree is a number, just return the number
    elif isinstance(tree, (int, float)):
        return tree
    # if the tree is a list, then we recurse on each element of the list
    # the first element should be an operation, and the remaining elements
    # should be arguments to pass to the operation.
    # return value is the result of calling operation on the args
    else:
        expressions = list(map(evaluate, tree))
        op = expressions[0]
        args = expressions[1:]
        if callable(op):
            return op(*args)
        else:
            raise SchemeEvaluationError(f"{op} not callable")


if __name__ == "__main__":
    # # code in this block will only be executed if lab.py is the main file being
    # # run (not when this module is imported)
    # import os

    # sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    # import schemerepl

    # schemerepl.SchemeREPL(
    #     sys.modules[__name__], use_frames=False, verbose=False
    # ).cmdloop()
    # s = "(define circle-area (lambda (r) (* 3.14 (* r r))))"
    s = "()"
    s = "(* 3.14 (* r r) ())"
    tokens = tokenize(s)
    print(tokens)
    parsed = parse(tokens)
    print(parsed)
    print(parse(["(", "+", "2", "(", "-", "5", "3", ")", "7", "8", ")"]))
    print(parse(["2"]))
