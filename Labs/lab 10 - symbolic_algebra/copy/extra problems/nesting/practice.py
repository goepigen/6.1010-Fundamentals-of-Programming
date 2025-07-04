"""
6.101 Mines Optional Practice Exercises: Nesting
"""

# no imports allowed!


def pascal(n):
    """
    Use recursion to create the first n rows of Pascal's Triangle.

    Parameters:
        * n (int) : a positive integer, representing the number of rows in triangle.

    Returns:
        A list of length n, where the element at index i is a list of ints
        representing the ith row of Pascal's triangle.

    >>> pascal(1)
    [[1]]
    >>> pascal(2)
    [[1], [1, 1]]
    >>> pascal(3)
    [[1], [1, 1], [1, 2, 1]]
    >>> pascal(4)
    # TODO: fill in expected result
    """
    raise NotImplementedError


def fill_n_cube(n):
    """
    Use recursion to make a cube of n layers of nested lists, where each layer is length n.
    The nth layer is an n-length list of zeroes.

    Parameters:
        * n (int) : a positive integer representing the length of each layer in the cube.

    Returns:
        A nested n-layer cube filled with zeroes.

    >>> fill_n_cube(1)
    [0]
    >>> fill_n_cube(2)
    [[0, 0], [0, 0]]
    >>> x = fill_n_cube(3)
    >>> x
    [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    >>> x[0][0][0] = 1  # make sure to avoid list aliasing!
    >>> x
    [[[1, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual practice.py functions.
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for pascal or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    # doctest.run_docstring_examples(
    #    pascal,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )

    # Your code below:
