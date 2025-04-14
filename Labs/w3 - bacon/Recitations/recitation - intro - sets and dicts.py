# This file contains some examples of how to work with sets and dictionaries
# (things we can do with these objects, what operations they support, etc)

# Some examples of operations on sets:
# (for more, see https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset )


# making sets

# from existing iterables
basket = ["apple", "orange", "apple", "pear", "orange"]
fruit1 = set(basket)

# directly
fruit1 = {"apple", "orange", "apple", "pear", "orange"}


# adding and removing elements (mutation)

fruit1.add("apple")
fruit1.add("banana")

fruit1.discard("grape")  # no exception if element not in set
fruit1.remove("apple")  # exception if element not in set


# comprehensions

with_n_in_name_list = [elt for elt in fruit1 if "n" in elt]  # list comprehension
with_n_in_name_set = {elt for elt in fruit1 if "n" in elt}  # set comprehension


# mathematical set operations: math notation, making new sets

fruit2 = {"orange", "apple", "berry", "grape", "orange"}
in_both = fruit1 & fruit2  # intersection
in_either = fruit1 | fruit2  # union
in_first_and_not_second = fruit1 - fruit2
in_second_and_not_first = fruit2 - fruit1
in_exactly_one = fruit1 ^ fruit2  # "symmetric difference"

# set operations: words, making new sets

fruit2 = {"orange", "apple", "berry", "grape", "orange"}
in_both = fruit1.intersection(fruit2)
in_either = fruit1.union(fruit2)
in_first_and_not_second = fruit1.difference(fruit2)
in_second_and_not_first = fruit2.difference(fruit1)
in_exactly_one = fruit1.symmetric_difference(fruit2)

# set operations: math notation, mutate the original set

fruit2 = {"orange", "apple", "berry", "grape", "orange"}
fruit1 &= fruit2  # in-place intersection
fruit1 |= fruit2  # in-place union
fruit1 -= fruit2  # in-place difference
fruit1 ^= fruit2  # in-place symmetric difference

# set operations: words, mutate original set

fruit2 = {"orange", "apple", "berry", "grape", "orange"}
fruit1.intersection_update(fruit2)  # in-place intersection
fruit1.update(fruit2)  # in-place union
fruit1.difference_update(fruit2)  # in-place difference
fruit1.symmetric_difference_update(fruit2)  # in-place symmetric difference


# more set operations

fruit1 = {"apple", "orange", "apple", "pear", "orange"}
fruit2 = {"orange", "apple", "berry", "grape", "orange"}
fruit3 = set()  # Create an empty set with 'set()', NOT with '{}'.
fruit3.add("banana")
fruit3.add("pear")
contained = fruit3.issubset(fruit1)
no_overlap = fruit3.isdisjoint(fruit2)
subsumes = fruit1.issuperset(fruit3)

# subset/superset relationships can be checked with math operators, too

check_subset = fruit3 < fruit1
check_proper_subset = fruit3 <= fruit1
check_superset = fruit3 > fruit1
check_proper_superset = fruit3 >= fruit1



# Some examples of using dictionaries:
# (for more, see https://docs.python.org/3/library/stdtypes.html#mapping-types-dict )

table = {}  # Create empty dictionary
table[27] = "my value"
table["dog"] = [1, 2, "three"]
table[27] = 3

if "dog" in table:  # key in dictionary?
    table["cat"] = "unhappy"

for key in table:
    print("key:", key)

for val in table.values():
    print("val:", val)

for key, val in table.items():
    print("key:", key, "-- val:", val)

del table[27]

cubes = {n: n**3 for n in range(8)}  # dictionary comprehension
xes = {n: "x" * n for n in range(8)}

table = {}
# "get" takes a key and a default value as input.  if the key is present, it
# returns the associated value.  if not, it returns the default value provided
# note that table[32] would give us an error here
val = table.get(32, [])
# note that we could have said val = table[32] if 32 in table else []
# but it's more concise with .get(...)
table[32] = "hello"
val = table.get(32, [])

table = {}
# "setdefault" works a lot like get, but it also has a side effect: if the
# given key was not in the dictionary, setdefault will associate the given key
# with the given default value inside the dictionary (such that future calls to
# get or setdefault will find that value)
table.setdefault(32, []).append(1)
table.setdefault(32, []).append(1)
table.setdefault(32, []).append(1)

# union operator can be used  with dictionaries as well

{"cat": 7} | {"dog": 8}  # makes a new dictionary with both key/val pairs

x = {"cat": 7}
x |= {"dog": 8, "ferret": 9}  # mutates x to add these new key/val pairs
