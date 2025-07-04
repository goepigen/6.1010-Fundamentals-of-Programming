import doctest


def sum_list(x):
    """
    Compute the sum of a list of numbers, recursively.

    >>> sum_list([1,2,3,4,5])
    15
    >>> sum_list([])
    0
    """
    if not x:
        return 0
    else:
        return x[0] + sum_list(x[1:])


def sum_nested(x):
    """
    >>> sum_nested([[1, 2], [3, [4, 5]], [[[[[6]]]]]])
    21
    >>> sum_nested([])
    0
    >>> sum_nested([[]])
    0
    """
    current_sum = 0

    for el in x:
        if isinstance(el, list):
            current_sum += sum_nested(el)
        else:
            current_sum += el
    return current_sum


def sum_nested2(x):
    """
    >>> sum_nested([[1, 2], [3, [4, 5]], [[[[[6]]]]]])
    21
    """
    if not x:
        return 0
    elif isinstance(x[0], list):
        return sum_nested2(x[0]) + sum_nested2(x[1:])
    else:
        return x[0] + sum_nested2(x[1:])


def subsequences(seq):
    """
    Given a tuple or list or other iterable, returns a set of tuples
    consisting of all its subsequences.
    A subsequence is a sequence of elements from seq that are in the
    same order as in seq but not necessarily adjacent.
    >>> sorted(subsequences([4,2,3]))
    [(), (2,), (2, 3), (3,), (4,), (4, 2), (4, 2, 3), (4, 3)]
    >>> sorted(subsequences(["x"]))
    [(), ('x',)]
    """
    if not seq:
        return {()}
    else:
        first = seq[0]
        rest = seq[1:]

        rest_seq = subsequences(rest)
        first_seq = {(first,) + sub_seq for sub_seq in rest_seq}

        return first_seq | rest_seq


def number_to_string(n, b):
    """
    Given an integer n (in base 10) and a base b (also in base 10) such
    that 2 <= b <= 10, returns n represented as a string in base-b notation.

    >>> number_to_string(5, 2)
    '101'
    >>> number_to_string(-829, 10)
    '-829'
    >>> number_to_string(0, 10)
    '0'
    """
    if n < b:
        return str(n)
    rem = n % b
    res = n // b
    return number_to_string(res, b) + str(rem)


if __name__ == "__main__":
    doctest.testmod(verbose=True)
