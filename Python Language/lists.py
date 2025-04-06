a = [1,2,3,4,5,6,7,8,9,10]

a[3:]
a[:3]
a[-3:]
a[:-3]

# shallow copy, same references
a[:]

# mutate by increasing length; returns None
a.append[11]

# add multiple elements to end of list with one call
# takes an iterable object
a.extend[[12,13]]

# add elements in the middle of a list
a.insert(2,55)

# removing elements 
# remove element at index N and returns it
a.pop(N)

# remove based on value
# takes object as input
# removes only earliest occurrence
# exception raised if object not in list
a.remove(55)

# concatenation

# concatenate two lists: make new list containing all original references
b = [100, 200]
a + b

## += behaves like extend
a += b # behaves like a.extend(b), ie mutates a

