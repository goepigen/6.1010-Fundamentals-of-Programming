# main difference relative to lists is that tuples are immutable
# once we have built a tuple, we cannot change any of the references in it, not can we
# add or remove items

t1 = (1,2,3)

# parentheses are not required
t2 = 1,2,3

# but are required when inside another list or tuple
[1,2, (4,3)]

# or in a print statement
print((1,2,3))


# the following is just an integer
(7)

# tuple
# trailing commas are ignored
7,
(7,)

# empty tuple
()
tuple()

