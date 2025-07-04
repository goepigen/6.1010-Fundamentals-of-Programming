"""
6.101 Recipes Optional Practice Exercise
Refactory - Recursion part 1
"""

# no imports allowed!


def count_subparts(part_manifest, part_num):
    """
    Recursively determine the number of total parts that will be needed to
    assemble the current part.

    Parameters:
        * part_manifest (dict<int, list<int>>) : a dictionary with integer part
            numbers mapping to a list of sub-part numbers needed to assemble the part.
            Each sub-part may or may not themselves be a key in the dictionary.
        * part_num (int) : the desired part to assemble.

    Returns:
        An integer representing the total number of subparts (including the 
        number of subparts of any compound subparts.

    >>> x = {1: [2, 3, 2, 3], 3: [2, 4, 5], 4: [2, 7]}
    >>> count_subparts(x, 3)
    5
    >>> count_subparts(x, 2)
    0
    >>> count_subparts(x, 1)
    14
    >>> y = {5: [1, 2], 3: [6,5,5,5,5], 7: [1,9], 10: [3,3,3,6]}
    >>> count_subparts(y, 10)
    0 # TODO FIX THIS
    """
    raise NotImplementedError("Implement me!")



def find_base_parts(part_manifest, part_num):
    """
    Recursively determine the unique base parts needed to assemble a part_num.

    Parameters:
        * part_manifest (dict<int, list<int>>) : a dictionary with integer part
            numbers mapping to a list of sub-part numbers needed to assemble the part.
            Each sub-part may or may not themselves be a key in the dictionary.
        * part_num (int) : the desired part to assemble.

    Returns:
        A set of integers representing the base parts needed to assemble the part.

    >>> x = {1: [2, 3, 2, 3, 6], 3: [2, 4, 5]}
    >>> list(sorted(find_base_parts(x, 3))) # returns a set {2, 4, 5}
    [2, 4, 5]
    >>> list(sorted(find_base_parts(x, 2))) # returns a set containing base part {2,}
    [2]
    >>> list(sorted(find_base_parts(x, 1))) # returns a set {2, 4, 5, 6}
    [2, 4, 5, 6]
    """
    raise NotImplementedError("Implement me!")


def maximum_steps(part_manifest):
    """
    Recursively determine the maximum number of assembly steps it would take to assemble
    a part in the manifest.

    Parameters:
        * part_manifest (dict<int, list<int>>) : a dictionary with integer part
            numbers mapping to a list of sub-part numbers needed to assemble the part.
            Each sub-part may or may not themselves be a key in the dictionary.

    Returns:
        An integer representing the maximum depth of the part_manifest.

    >>> maximum_steps({1: [2, 3, 2, 3], 3: [2, 4, 5]})
    2
    >>> maximum_steps({3: [2, 4, 5]})
    1
    >>> maximum_steps({2: [1], 4: [3, 2], 3: [2, 1]})
    3
    >>> maximum_steps({5: [1, 2], 3: [6,5,5,5,5], 7: [1,9], 10: [3,3,3,6]})
    3
    """

    def max_helper(part_num):
        """
        Given a part_num (int), return the maximum number of assembly steps.
        Base parts (parts that have no sub-parts) have 0 assembly steps.
        """
        return 0

    raise NotImplementedError("Implement me!")


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual practice.py functions.
    import doctest

    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags, verbose=False)  # runs ALL doctests
    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for count_subparts or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    """
    doctest.run_docstring_examples(
        count_subparts,
        globals(),
        optionflags=_doctest_flags,
        verbose=True
    )
    """
    # Your code below:
