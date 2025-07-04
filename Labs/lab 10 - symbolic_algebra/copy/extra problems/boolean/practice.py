"""
6.101 Lisp 1 Optional Practice Exercises: Boolean
"""

def expand(text):
    """
    Given a string text, multiply it according to the integers
    followed by individual characters, or multiply sections
    surrounded by {}.

    >>> expand("a")
    'a'
    >>> expand("b6a")
    'baaaaaa'
    >>> expand("2ab3cd")
    'aabcccd'
    >>> expand("3{cat}dog")
    'catcatcatdog'
    >>> expand("3{2{2ac}d}4e")
    'aacaacdaacaacdaacaacdeeee'
    """
    def expand_helper(idx):
        char = text[idx]
        if char.isdigit():
           pass
        elif char == '{':
           pass
        else:
           pass
         
    out, index = "", 0
    while index < len(text):
        substring, index = expand_helper(index)
        out += substring

    return out


def tokenize_bool(expression):
    """
    Parameters:
        * expression: a string consisting of boolean values 1 (True) and 0
            (False), as well as operands and, or, and ! (not).

    Returns:
        A list of strings representing the individual operands and values.

    >>> tokenize_bool("1")
    ['1']
    >>> tokenize_bool("! 0 ")
    ['!', '0']
    >>> tokenize_bool("or 1 0")
    ['or', '1', '0']
    >>> tokenize_bool("and or 1 0 1 ! 1")
    ['and', 'or', '1', '0', '1', '!', '1']
    >>> tokenize_bool("! ! and or 1 0 1 or ! 1 1")
    ['!', '!', 'and', 'or', '1', '0', '1', 'or', '!', '1', '1']
    """
    raise NotImplementedError


def parse_bool(tokens):
    """
    Parameters:
        * tokens: list of str representing individual operands and values.

    Returns:
        If the token represents a boolean value, return the boolean value.
        Otherwise return a list representing the boolean expression (which may
        contain operands, booleans and lists representing sub-expressions).

    >>> parse_bool(['1'])
    True
    >>> parse_bool(['!', '0'])
    ['!', False]
    >>> parse_bool(['or', '1', '0'])
    ['or', True, False]
    >>> parse_bool(['and', '1', 'or', '1', '0'])
    ['and', True, ['or', True, False]]
    >>> parse_bool(['and', 'or', '1', '0', '1', '!', '1'])
    ['and', ['or', True, False, True, ['!', True]]]
    >>> parse_bool(['!', '!', 'and', 'or', '1', '0', '1', 'or', '!', '1', '1'])
    ['!', ['!', ['and', ['or', True, False, True], ['or', ['!', True], True]]]]
    """

    def parse_helper(index):
        """
        Given the index of an expression, return a tuple containing the
        parsed expression starting at that index and the index representing
        the end index of the expression + 1.
        """
        raise NotImplementedError

    result, index = parse_helper(0)
    return result



if __name__ == "__main__":
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests