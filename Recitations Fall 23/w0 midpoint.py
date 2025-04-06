# 6.101 recitation 0


# testing and debugging, some python "goodies" and style


############### EXAMPLE 1: REVERSING NESTED LISTS


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





# if __name__ == '__main__':
#     x = [[1, 2], [3, 4]]
#     print(reverse_all(x))
#     y = [[1, 2, 8], [3, 4, 9]]
#     print(reverse_all(y))





############### EXAMPLE 2: ADDING ELEMENTS IN NESTED LISTS


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




# if __name__ == '__main__':
#     print('actually', sum_lists([[50, 100], [5, 6, 7]]))
#     print('expected', [150, 18])







# def test_sum_lists():
#     assert sum_lists([[50, 100], [5, 6, 7]]) == [150, 18]






############### EXAMPLE 3: SUBTRACTING CORRESPONDING ELEMENTS IN LISTS


def subtract_lists(l1, l2):
    """
    Given lists of numbers l1 and l2, return a new list where each position is
    the difference between that position in l1 and in l2.
    """
    output = []
    for i in range(len(l1)):
        output.append(l1[i] - l2[i])
    return output






# def test_subtract_lists():
#     assert subtract_lists([1, 2], [3, 5]) == [-2, -3]
#     assert subtract_lists([325, 64, 66], [1, 2, 3]) == [324, 62, 63]
