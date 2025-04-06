# Create a dictionary
tel = {'jack': 4098, 'sape': 4139}

# Set a value for a new key
tel["jack"] = 4127

# Get a value at a key
tel["jack"]

# Delete a key: value pair
del tel['sape']

# List of keys in the dictionary
list(tel)

# List of keys in alphabetical order
sorted(tel)

# Check if a key is in the dictionary
'jack' in tel

# Alternative way to build a dictionary, using the dict() constructor
dict([('sape', 4139), ('guido', 4322)])

# or, using keyword arguments
dict(sape=4139, guido=4322)

# Alternative way to build a dictionary, using list comprehension
{ x: x**2 for x in (2, 4, 6) }

# Looping through dictionaries

# Use items() to get both key and value at the same time
knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.items():
    print(k, v)



