# 6.101 recitation

# testing and debugging, some python "goodies" and style


############### EXAMPLE 0: ADDING ELEMENTS IN NESTED LISTS


def sum_lists(lists):
    """
    Given a list of lists, return a new list where each list is replaced by
    the sum of its elements.
    """
    output = [0] * len(lists)
    for i in range(len(lists)):
        total = 0
        for i in lists[i]:
            total += i
        output[i] = total
    return output


# Which of the following, if any, are issues() with the code as written?
#
# A: [0] * len(lists) creates a data structure with aliasing
# B: Cannot mutate output once it has been created
# C: The lengths of the inner lists are different
# D: Inner loop variable "shadows" outer loop variable
# E: The variable total accumulates across multiple lists


############### EXAMPLE 1: REVERSING NESTED LISTS

def reverse_list_of_lists(input):
    new_list = []
    for l in input:
        new_list.append(l[::-1])
    return new_list


def reverse_all(inp):
    """
    given a list of lists, return a new list of lists
    but with all of the inner lists reversed, without
    modifying the input list

    example:
    >>> input1 = [[1, 2], [3, 4]]
    >>> reverse_all(input1)
    [[2, 1], [4, 3]]
    """
    output = inp
    for L in output:
        L.reverse()
    return output


def test_reverse():
    input1 = [[1, 2], [3, 4]]
    output1 = [[2, 1], [4, 3]]
    assert reverse_all(input1) == output1
    assert reverse_all(reverse_all(input1)) == input1

    input2 = [[1, 2, 8], [3, 4, 9]]
    output2 = [[8, 2, 1], [9, 4, 3]]
    assert reverse_all(input2) == output2
    assert reverse_all(reverse_all(input2)) == input2

    print('test_reverse: All tests passed')


############### EXAMPLE 2: SUBTRACTING CORRESPONDING ELEMENTS IN LISTS


def subtract_lists(l1, l2):
    """
    given lists of numbers l1 and l2, return a new list where each position is
    the difference between that position in l1 and in l2.
    """
    output = []
    for i in range(len(l1)):
        output.append(l1[i] - l2[i])
    return output


def test_subtract_lists():
    assert subtract_lists([1, 2], [3, 5]) == [-2, -3]
    assert subtract_lists([325, 64, 66], [1, 2, 3]) == [324, 62, 63]
    print('test_subtract_lists: All tests passed')
