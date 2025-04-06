# 6.101 recitation: lab 1 midpoint




#################### lab1 data representation

# i is a 2x3 grayscale image
i = {
    'height': 3,
    'width': 2,
    'pixels': [0, 50, 50, 100, 100, 255],
}










#################### some lab1 debugging

def get_pixel(image, row, col):
    return image["pixels"][col, row]


def set_pixel(image, row, col, color):
    image["pixels"][col, row] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "widht": image["width"],
        "pixels": [],
    }
    for col in range(image["height"]):
        for row in range(image["width"]):
            color = get_pixel(image, col, row)
            new_color = func(color)
        set_pixel(result, row, col, new_color)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda color: 256-color)

def test_inverted_2():
    image = {
        'height': 3,
        'width': 2,
        'pixels': [0, 50, 50, 100, 100, 255],
    }
    result = inverted(image)
    assert False # haven't finished this

# simulate all the other failing tests
def test_inverted_1():
    raise NotImplementedError
def test_inverted_images_mushroom():
    raise NotImplementedError
def test_inverted_images_twocats():
    raise NotImplementedError
def test_inverted_images_chess():
    raise NotImplementedError
def test_blurred_images_mushroom_1():
    raise NotImplementedError
def test_blurred_images_mushroom_3():
    raise NotImplementedError
def test_blurred_images_mushroom_7():
    raise NotImplementedError
def test_blurred_images_twocats_1():
    raise NotImplementedError
def test_blurred_images_twocats_3():
    raise NotImplementedError
def test_blurred_images_twocats_7():
    raise NotImplementedError
def test_blurred_images_chess_1():
    raise NotImplementedError
def test_blurred_images_chess_3():
    raise NotImplementedError
def test_blurred_images_chess_7():
    raise NotImplementedError
def test_blurred_black_image():
    raise NotImplementedError
def test_blurred_centered_pixel():
    raise NotImplementedError
def test_sharpened_images_mushroom_1():
    raise NotImplementedError
def test_sharpened_images_mushroom_3():
    raise NotImplementedError
def test_sharpened_images_mushroom_9():
    raise NotImplementedError
def test_sharpened_images_twocats_1():
    raise NotImplementedError
def test_sharpened_images_twocats_3():
    raise NotImplementedError
def test_sharpened_images_twocats_9():
    raise NotImplementedError
def test_sharpened_images_chess_1():
    raise NotImplementedError
def test_sharpened_images_chess_3():
    raise NotImplementedError
def test_sharpened_images_chess_9():
    raise NotImplementedError
def test_edges_images_mushroom():
    raise NotImplementedError
def test_edges_images_twocats():
    raise NotImplementedError
def test_edges_images_chess():
    raise NotImplementedError
def test_edges_centered_pixel():
    raise NotImplementedError






############### Iterables

# how would you rewrite this so it is more "pythonic"?

for i in [0, 1, 2, 3, 4, 5]:
    print(i**2)












# how would you rewrite these loops to be more pythonic?

movies =  [ 'Alien', 'Barbie', 'Clue', 'Frozen', 'Inception' ]
ratings = [     8.5,      7.3,    7.2,      7.4,        8.8,    3.3,    1.5 ]

for i in range(len(movies)-1, -1, -1):
    print(movies[i])

for i in range(len(movies)):
    print(i, movies[i])

n = min(len(movies), len(ratings))
for i in range(n):
    print(movies[i], ratings[i])









# how would you rewrite poly_evaluate() to be more pythonic?

def poly_evaluate(p, x):
    """
    given an n-element list of floats p which are polynomial coefficients,
    and a float value x,
    returns the value of the polynomial p[0]x^0 + p[1]x^1 + ... p[n-1]x^(n-1)
    """
    answer = 0
    for i in range(len(p)):
        answer += p[i] * x ** i
    return answer

poly_evaluate([7, 1, 2], 20)









################### One-liners

# can you rewrite this to compute `result` in only one line?
result = 0
for i in range(20):
    s = i**2
    result += s

# can you rewrite this into just a one-line `return` statement?
def average(numbers):
    total = 0
    count = 0
    for x in numbers:
        total += x
        count += 1
    return total / count






#################### sorting

colors = ['red', 'green', 'blue', 'yellow', 'chartreuse', 'periwinkle']

# how can we write this in one line?

new_colors = colors.copy()
new_colors.sort()
result = ''
for color in new_colors:
    result += color + ' '
result = result[:-1] # remove trailing space, if any


# what if we want to sort by the number of letters in the color's name instead?
#  so red (3) comes first, periwinkle (10) is last

