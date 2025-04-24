# 6.101 recitation: recursion warmup


############################# Visualizing & debugging recursion


from debug_recursion import show_recursive_structure
import sys

sys.setrecursionlimit(10_000)  # by default 1000


@show_recursive_structure
def list_sum(x):
    if not x:
        return 0
    return x[0] + list_sum(x[1:])


print(list_sum([9, 8, 7, 6]))

# @ show_recursive_structure
# def list_sum_2(x, sofar=0):
#     if not x:
#         raise NotImplementedError  # TODO: what here?
#     return list_sum_2(x[1:], sofar+x[0])
#
# print(list_sum_2([9, 8, 7, 6]))


############################# Trees

t1 = {"value": 3, "children": []}

t2 = {
    "value": 9,
    "children": [
        {"value": 2, "children": []},
        {"value": 3, "children": []},
        {"value": 7, "children": []},
    ],
}

t3 = {
    "value": 9,
    "children": [
        {"value": 2, "children": []},
        {
            "value": 3,
            "children": [
                {"value": 99, "children": []},
                {"value": 16, "children": [{"value": 7, "children": []}]},
                {"value": 42, "children": []},
            ],
        },
    ],
}


def tree_max(tree):
    """
    If tree is a dict {value: number, children: list of trees},
    returns the maximum value found in the tree
    """
    pass
