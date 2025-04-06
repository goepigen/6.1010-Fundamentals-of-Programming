"""
6.101 Lab 1:
Image Processing
"""

#!/usr/bin/env python3

import math

import os

from PIL import Image

TEST_DIRECTORY = os.path.dirname(__file__)

# NO ADDITIONAL IMPORTS ALLOWED!

# HELPERS


def flat_index_boundary_behavior_zero(image, row, col):
    width = image["width"]
    height = image["height"]

    if (row < 0) or (col < 0) or (row > height - 1) or (col > width - 1):
        return 0

    return flat_index(width, row, col)


def flat_index_boundary_behavior_extend(image, row, col):
    width = image["width"]
    height = image["height"]

    if row < 0:
        if col < 0:
            i = flat_index(width, 0, 0)
        elif col > width - 1:
            i = flat_index(width, 0, width - 1)
        else:
            i = flat_index(width, 0, col)
    elif row > height - 1:
        if col < 0:
            i = flat_index(width, height - 1, 0)
        elif col > width - 1:
            i = flat_index(width, height - 1, width - 1)
        else:
            i = flat_index(width, height - 1, col)
    else:
        if col < 0:
            i = flat_index(width, row, 0)
        elif col > width - 1:
            i = flat_index(width, row, width - 1)
        else:
            i = flat_index(width, row, col)

    return i


def flat_index_boundary_behavior_wrap(image, row, col):
    width = image["width"]
    height = image["height"]

    if row < 0:
        if col < 0:
            i = flat_index(width, height + row, width + row)
        elif col > width - 1:
            i = flat_index(width, height + row, col - width)
        else:
            i = flat_index(width, height + row, col)
    elif row > height - 1:
        if col < 0:
            i = flat_index(width, height - row, width + col)
        elif col > width - 1:
            i = flat_index(width, height - row, col - width)
        else:
            i = flat_index(width, height - row, col)
    else:
        if col < 0:
            i = flat_index(width, row, width + col)
        elif col > width - 1:
            i = flat_index(width, row, col - width)
        else:
            i = flat_index(width, row, col)

    return i


def get_pixel(image, row, col, boundary_behavior="zero"):
    """
    Given image and a (row, col) location, return pixel associated with that location
    in a 1-d list of pixel values stored in row-major order

    Parameters:
        * row (int): row number to look up, with 0 being top-most
        * col (int): col number to look up, with 0 being left-most

    Returns the integer representing a pixel from a row-major-order 1-d list of pixels that
    corresponds to the location (row, col)
    """

    match boundary_behavior:
        case "zero":
            i = flat_index_boundary_behavior_zero(image, row, col)
        case "extend":
            i = flat_index_boundary_behavior_extend(image, row, col)
        case "wrap":
            i = flat_index_boundary_behavior_wrap(image, row, col)

    return image["pixels"][i]


def set_pixel(image, row, col, color):
    i = flat_index(image["width"], row, col)
    image["pixels"][i] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [0 for _ in range(image["height"] * image["width"])],
    }
    for row in range(image["height"]):
        for col in range(image["width"]):
            color = get_pixel(image, row, col)
            new_color = func(color)
            set_pixel(result, row, col, new_color)
    return result


def box_blur_kernel(n):
    return {"size": n, "weights": [1 / (n * n) for _ in range(n * n)]}


def sharpen_kernel(n):
    kernel = {"size": n, "weights": [-1 / (n * n) for _ in range(n * n)]}

    mid = int((n - 1) / 2)

    kernel["weights"][flat_index(n, mid, mid)] += 2

    return kernel


def flat_index(width, row, col):
    """
    Given image and a (row, col) location, return index associated with that location
    in a 1-d list of pixel values stored in row-major order

    Parameters:
        * row (int): row number to look up, with 0 being top-most
        * col (int): col number to look up, with 0 being left-most

    Returns the integer representing index into a row-major-order 1-d list of pixel values
    that corresponds to the location (row, col)
    """
    return row * width + col


def get_kernel_weight(kernel, row, col):
    return kernel["weights"][flat_index(kernel["size"], row, col)]


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the "pixels" list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    result = {"height": image["height"], "width": image["width"], "pixels": []}

    for pixel in image["pixels"]:
        rounded_pixel = round(pixel)
        if pixel > 255:
            rounded_pixel = 255
        elif pixel < 0:
            rounded_pixel = 0
        result["pixels"].append(rounded_pixel)

    return result


# FILTERS


def inverted(image):
    return apply_per_pixel(image, lambda color: 255 - color)


def correlate(image, kernel, boundary_behavior, clip_and_round=True):
    """
    Given an image, a kernel and an option for how to deal with pixels near the boundary of the image,
    apply kernel to image via a correlation (brightness of a pixel in the correlated image is expressed as
    linear combination) of pixels around it (the exact number of pixels determined by the kernel).

    After applying kernel, round the resulting pixel values and clip them (values above 255 become 255) and
    values below 0 become 0.

    Parameters:
        * image: dictionary of form {
            height: int,
            width: int,
            pixels: array of int
        }
        * kernel: a dictionary with form {
            size: int,
            weights: size x size 1-d array
        }
        * boundary_behavior: one of "zero", "wrap", "extend"

    Returns a new image dictionary representing the result of the correlation
    """

    extra_pixels = int((kernel["size"] - 1) / 2)

    result = {"height": image["height"], "width": image["width"], "pixels": []}

    for row in range(image["height"]):
        for col in range(image["width"]):
            pixel = 0
            for i in range(kernel["size"]):
                for j in range(kernel["size"]):
                    kernel_weight = get_kernel_weight(kernel, i, j)
                    image_pixel = get_pixel(
                        image,
                        row + i - extra_pixels,
                        col + j - extra_pixels,
                        boundary_behavior,
                    )
                    pixel += kernel_weight * image_pixel
            result["pixels"].append(pixel)

    clipped_and_rounded = round_and_clip_image(result) if clip_and_round else result
    return clipped_and_rounded


def blurred(image, kernel_size):
    """
    Return a new image representing the result of applying a box blur (with the
    given kernel size) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)

    # then compute the correlation of the input image with that kernel

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.

    kernel = box_blur_kernel(kernel_size)

    blurred_image = correlate(image, kernel, "extend")

    return round_and_clip_image(blurred_image)


# SHARPENING


def sharpened(image, n):
    """
    Given an image and a kernel size n, apply an unsharp mask


    """
    kernel = sharpen_kernel(n)

    sharpened = correlate(image, kernel, "extend")

    return sharpened


def edges(image):
    k1 = {"size": 3, "weights": [-1, -2, -1, 0, 0, 0, 1, 2, 1]}
    k2 = {"size": 3, "weights": [-1, 0, 1, -2, 0, 2, -1, 0, 1]}

    r1 = correlate(image, k1, "extend", False)
    r2 = correlate(image, k2, "extend", False)

    height = image["height"]
    width = image["width"]
    length = height * width

    result = {"height": height, "width": width, "pixels": [0 for _ in range(length)]}

    for i in range(length):
        result["pixels"][i] = math.sqrt(r1["pixels"][i] ** 2 + r2["pixels"][i] ** 2)

    return round_and_clip_image(result)


# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.

    # im = load_greyscale_image(os.path.join(TEST_DIRECTORY, 'test_images', 'bluegill.png'))
    # result = inverted(im)
    # save_greyscale_image(result, os.path.join(TEST_DIRECTORY, 'test_images_inv', 'bluegill_inv.png'))

    im = load_greyscale_image(
        os.path.join(TEST_DIRECTORY, "test_images", "pigbird.png")
    )

    k1 = {"size": 3, "weights": [-1, -2, -1, 0, 0, 0, 1, 2, 1]}
    k2 = {"size": 3, "weights": [-1, 0, 1, -2, 0, 2, -1, 0, 1]}

    r1 = correlate(im, k1, "extend")
    r2 = correlate(im, k2, "extend")

    save_greyscale_image(
        r1, os.path.join(TEST_DIRECTORY, "test_images_correlated", "pigbird_k1.png")
    )
    save_greyscale_image(
        r2, os.path.join(TEST_DIRECTORY, "test_images_correlated", "pigbird_k2.png")
    )
