# 6.101 recitation: recursion warmup


############################# Visualizing & debugging recursion


from debug_recursion import show_recursive_structure
import sys

# sys.setrecursionlimit(10_000)  # by default 1000


# @show_recursive_structure
def fib(n):
    if n <= 2:
        return 1
    return fib(n-1) + fib(n-2)

print(fib(5))
# print(f"{fib._count=}")
# print(f"{fib._max_depth=}")









############################# Trees

t1 = {'value': 3,
      'children': []}

t2 = {'value': 9,
      'children': [{'value': 2, 'children': []},
                   {'value': 3, 'children': []},
                   {'value': 7, 'children': []}]}

t3 = {'value': 9,
      'children': [{'value': 2, 'children': []},
                   {'value': 3,
                    'children': [{'value': 99, 'children': []},
                                 {'value': 16,
                                  'children': [{'value': 7, 'children': []}]},
                                 {'value': 42, 'children': []}]}]}

def tree_max(tree):
    """
    If tree is a dict { value: number, children: list of trees },
    returns the maximum value found in the tree
    """
    pass











# @show_recursive_structure
def tree_max(tree):
    if not tree['children']:
        return tree['value']
    else:
        max_so_far = tree['value']
        for child in tree['children']:
            max_so_far = max(max_so_far, _________)
        return max_so_far

# print(tree_max(t1))
# print(tree_max(t2))
# print(tree_max(t3))







