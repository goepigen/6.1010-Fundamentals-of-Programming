"""
6.101 Lisp 2 Optional Practice Exercises: Loopless
"""


"""
Translating LISP Exercise:
What is the equivalent python code for the following Scheme program?

(define (call x) (x))
(define (spam) (call (lambda () 2)))
(call spam)
"""
# your code here

def map(tup_link, func):
    """
    Given a linked list and a function that takes a single argument, create
    a new linked list containing the results of applying the given
    function to each element of the given list.

    For example:
    >>> map((1, (2, (3, (4, (5, None))))), lambda x: x*x)
    (1, (4, (9, (16, (25, None)))))
    >>> map((1, None), lambda x: -x)
    (-1, None)
    >>> map(("zebra", ("ran", ("backwards", None))), lambda x: x[0]+"oom!")
    ('zoom!', ('room!', ('boom!', None)))
    """
    raise NotImplementedError


# Bonus exercise: translate your python map function to LISP!
MAP_LISP = """


"""


def filter(tup_link, func):
    """
    Given a linked list and filter function, create a new linked list containing
    the values that pass through the filter.

    The filter function takes a value and returns a boolean indicating whether
    the value should be included in the result.

    For example:
    >>> filter((1, (2, (3, (4, (5, None))))), lambda x: x%2 == 0)
    (2, (4, None))
    >>> filter((1, None), lambda x: x < 0) is None
    True
    >>> map(filter(("zebra", ("ran", ("backwards", ("", None)))), lambda x: len(x) > 3), lambda x: x[0]+"oom!")
    ('zoom!', ('boom!', None))
    """
    raise NotImplementedError


# Bonus exercise: translate your python filter function to LISP!
FILTER_LISP = """


"""


def reduce(tup_link, func, val):
    """
    Given a linked list, a function, and an initial value as inputs, make the
    output by successively applying the given function to theelements in the
    list, maintaining an intermediate result along the way.

    This is perhaps the most difficult of the three functions to understand,
    but it may be easiest to see by example:
    >>> reduce((1, (2, (3, (4, None)))), lambda val, x: val + x, 0)
    10
    >>> reduce(("zebra", ("ran", ("backwards", ("", None)))), lambda val, x: val + " " + x, "the")
    'the zebra ran backwards '
    """
    raise NotImplementedError


# Bonus exercise: translate your python filter function to LISP!
REDUCE_LISP = """


"""


if __name__ == "__main__":
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # your code here
