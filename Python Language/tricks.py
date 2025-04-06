x = [1, 2, 3, 4]
y = [100, 200, 300, 400]

# Tuple unpacking of zip
for x_val, y_val in zip(x,y):
    print(x_val + y_val)

# * unpacking operator

location = (0,1)

def add(x, y):
    return x + y

add(*location)

# ternary

# EXPR if CONDITION else OTHER_CONDITION

l = [-1,3,4,-5,7]

r = [(-val if val < 0 else val) for val in l]

print(r)

[y*y for y in l]

l1 = [1,2,3,4]
l2 = [5,6,7,8,9]

r = [i - j for i, j in zip(l1,l2)]

print(r)