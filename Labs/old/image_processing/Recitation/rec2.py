# 6.101 recitation: lab 1 wrapup



############### Data representation

# image representation
i = {
    'height': 3,
    'width':  2,
    'pixels': [ 0, 50, 50, 100, 100, 255 ],
}
def get_pixel(image, row, col):
    return image["pixels"][row*image["width"] + col]
def set_pixel(image, row, col, color):
    image["pixels"][row*image["width"] + col] = color



# how to represent a kernel?
# (a kernel is a square, odd-sized matrix of float values)

# like an image?
kernel = {
    'height': 3,
    'width':  3,
    'pixels': [0, 0, 0, 0, 0, 0, 0, 1, 0 ],
}

# OR:
kernel = [0, 0, 0, 0, 0, 0, 0, 1, 0 ]

# OR:
kernel = [
    [0, 0, 0], 
    [0, 0, 0], 
    [0, 1, 0],
]

# OR:
kernel = {
    (-1,-1): 0,   (-1,0): 0,   (-1,1): 0,
    (0,-1):  0,   (0,0):  0,   (0,1):  0,
    (1,-1):  0,   (1,0):  1,   (1,1):  0,
}







# core of the correlation algorithm...

# ... when kernel represented as list of lists, making a square 2D matrix
def compute_output_at(image, kernel, row, col):
    """
    returns output pixel at row, col
    """
    output_pixel = 0
    n = len(kernel)
    center = n // 2
    for kernel_row in range(n):
        for kernel_col in range(n):
            dr = kernel_row - center
            dc = kernel_col - center
            output_pixel += get_pixel(image, row + dr, col + dc) * kernel[kernel_row][kernel_col]
    return output_pixel

# ... when kernel represented as dictionary, with (dr,dc) => kernel value at that offset in the kernel
def compute_output_at(image, kernel, row, col):
    output_pixel = 0
    for dr,dc in kernel:
        output_pixel += get_pixel(image, row + dr, col + dc) * kernel[dr,dc]
    return output_pixel






# create the coordinate-dictionary representation from a 2D array representation
kernel = make_kernel([  
    [0, 0, 0], 
    [0, 0, 0], 
    [0, 1, 0],
])

def make_kernel(matrix):
    """
    Takes an odd square 2D matrix (a list of rows, where each row is a list of floats)
    and returns a coordinate dictionary (dr,dc) => float,
                 where the origin (0,0) is the center cell of the matrix
    """
    n = len(matrix)
    center = n // 2
    kernel = {}
    for row in range(n):
        for col in range(n):
            kernel____ = matrix____
    return kernel









############### Boundary behaviors

# lab 1 recommended putting boundary behavior into get_pixel(image, row, col)

# but what if we handled different boundary behaviors this way instead?

def correlate(image, kernel, boundary_behavior):
    if boundary_behavior == "zero":
        ... # 30 lines of correlation algorithm, but using zero boundary behavior
    elif boundary_behavior == "extend":
        ... # basically same 30 lines of correlation algorithm, but using extend boundary behavior
    elif boundary_behavior == "wrap":
        ... # basically same 30 lines of correlation algorithm, but using wrap boundary behavior







# or this way?

def correlate(image, kernel, boundary_behavior):
    # first make bigger_image by extending image with len(kernel)/2+1 more pixels around each edge,
    # filled with appropriate pixel values for boundary behavior
    ...

    # then run correlation algorithm on bigger_image, keeping sliding window inside it
    ...









# focusing on the get_pixel() approach

# what's good?
# what to improve?
# buggy?

def get_pixel(image, row, col, boundary_behavior):
    if boundary_behavior == "zero":
        if row < 0:
            return 0
        elif row >= image["height"]:
            return 0
        elif col < 0:
            return 0
        elif col >= image["width"]:
            return 0
        if row >= 0:
            if row < image["height"]:
                if col >= 0:
                    if col < image["width"]:
                        return image['pixels'][((row * image["width"]) + col)]
    elif boundary_behavior == "extend":
        ...
    elif boundary_behavior == "wrap":
        ...








# what's good?
# what to improve?
# buggy?

def get_pixel(image, row, col, boundary_behavior):
    if boundary_behavior == "zero":
        if 0 <= row < image["height"] and 0 <= col < image["width"]:
            return image['pixels'][((row * image["width"]) + col)]
        else:
            return 0
    elif boundary_behavior == "extend":
        if row < 0:
            row = 0
        if row >= image["height"]:
            row = image["height"]-1
        if col < 0:
            col = 0
        if col >= image["width"]:
            col = image["width"]-1
        return image['pixels'][((row * image["width"]) + col)]
    elif boundary_behavior == "wrap":
        ...
