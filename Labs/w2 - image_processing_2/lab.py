"""
6.101 Lab 2:
Image Processing 2
"""

#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image

# VARIOUS FILTERS


def inverted(image):
    return apply_per_pixel(image, lambda color: 255 - color)


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


def sharpened(image, n):
    """
    Given an image and a kernel size n, apply an unsharp mask


    """
    kernel = sharpen_kernel(n)

    sharpened_image = correlate(image, kernel, "extend")

    return sharpened_image


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


# HELPERS


def box_blur_kernel(n):
    return {"size": n, "weights": [1 / (n * n) for _ in range(n * n)]}


def sharpen_kernel(n):
    kernel = {"size": n, "weights": [-1 / (n * n) for _ in range(n * n)]}

    mid = int((n - 1) / 2)

    kernel["weights"][flat_index(n, mid, mid)] += 2

    return kernel


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
        # More concise alternative is
        # rounded_pixel = max(0, min(255, round(pixel)))
        result["pixels"].append(rounded_pixel)

    return result


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


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """

    def create_image_from_pixels(pixels, height, width):
        return {"height": height, "width": width, "pixels": pixels}

    def color_filter(image):
        pixels = image["pixels"]

        # Split list of (r, g, b) tuples into three greyscale images
        red, green, blue = [
            create_image_from_pixels(p, image["height"], image["width"])
            for p in list(zip(*pixels))
        ]

        filtered_red = filt(red)
        filtered_green = filt(green)
        filtered_blue = filt(blue)

        new_pixels = list(
            zip(
                filtered_red["pixels"],
                filtered_green["pixels"],
                filtered_blue["pixels"],
            )
        )

        new_image = {
            "height": image["height"],
            "width": image["width"],
            "pixels": new_pixels,
        }

        return new_image

    return color_filter


def make_blur_filter(kernel_size):
    return lambda image: blurred(image, kernel_size)


def make_sharpen_filter(kernel_size):
    return lambda image: sharpened(image, kernel_size)


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """

    def combine_filters(image):
        processed_image = image
        for f in filters:
            processed_image = f(processed_image)

        return processed_image

    return combine_filters
    # return lambda image: reduce(lambda img, f: f(img), filters, image)


# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image. Returns a new image.
    """

    carved = image.copy()

    for _ in range(ncols):
        grey = greyscale_image_from_color_image(carved)
        energy = compute_energy(grey)
        cem = cumulative_energy_map(energy)
        seam = minimum_energy_seam(cem)
        carved = image_without_seam(carved, seam)

    return carved


# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """

    greyscale_image = {
        "height": image["height"],
        "width": image["width"],
        "pixels": [
            round(0.299 * r + 0.587 * g + 0.114 * b) for r, g, b in image["pixels"]
        ],
    }

    return greyscale_image


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    width = energy["width"]
    height = energy["height"]

    cem = energy.copy()

    # First row of cumulative energy is just the energy.
    cem["pixels"] = energy["pixels"][:width]

    for row in range(1, height):
        # last width pixels in the current cem is the row in the cem before the one being built currently
        row_above_ce = cem["pixels"][-width:]
        for col in range(width):
            cols_neighbors_above = get_upper_neighbor_cols(col, width)
            upper_neighbors_ce = [row_above_ce[c] for c in cols_neighbors_above]
            smallest_neighbor_ce = min(upper_neighbors_ce)
            current_energy = energy["pixels"][flat_index(width, row, col)]
            cumul_energy = current_energy + smallest_neighbor_ce
            cem["pixels"].append(cumul_energy)

    return cem


def get_upper_neighbor_cols(col, width):
    potential_upper_neighbors = [col - 1, col, col + 1]

    return [p for p in potential_upper_neighbors if p >= 0 and p < width]


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of lists where the inner lists
    contain two elements: the row in the image and the position of the pixel in
    that row with the minimum energy.

    Args:
        cem: a cumulative energy map
    Returns a list of lists containing [row number, position] elements.
    """
    width = cem["width"]
    height = cem["height"]
    pixels = cem["pixels"]

    last_row_start = (height - 1) * width
    last_row = pixels[last_row_start:]
    last_row_i = height - 1

    min_col = min(range(width), key=lambda c: last_row[c])

    seam = [[last_row_i, min_col]]

    for row in range(last_row_i - 1, -1, -1):
        current_col = seam[-1][1]
        cols_neighbors_above = get_upper_neighbor_cols(current_col, width)
        min_col = min(
            cols_neighbors_above, key=lambda c: pixels[flat_index(width, row, c)]
        )

        seam.append([row, min_col])

    return [flat_index(width, r, c) for r, c in seam]


def get_row(image, i):
    """
    Given an image, returns row i of the pixels in the image.

    Parameters:
        image: Image object,
        i: integer, represents index of row to obtain

    Returns list containing elements of the ith row of the pixels of image.
    """
    width = image["width"]
    return image["pixels"][i * width : i * width + width]


def find_min(l):
    """
    Finds the minimum element in a list and returns the index and value of this element.

    Parameters:
        l: list

    Returns:
        min_i: integer, index of minimum element
        min_el: integer, value of minimum element
    """
    min_i = 0
    min_el = l[min_i]

    for i, el in enumerate(l):
        if el < min_el:
            min_i = i
            min_el = el

    return min_i, min_el


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    pixels = image["pixels"]
    seam_set = set(seam)

    new_pixels = [p for i, p in enumerate(pixels) if i not in seam_set]

    new_image = {
        "width": image["width"] - 1,
        "height": image["height"],
        "pixels": new_pixels,
    }

    return new_image


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
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
    by the 'mode' parameter.
    """
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_data(file_path):
    import pickle

    file = open(file_path, "rb")

    data = pickle.load(file)

    file.close()

    return data


# if __name__ == "__main__":
#     im = load_color_image("test_images/twocats.png")
#     res = seam_carving(im, 100)
#     save_color_image(res, "test_personal_results/twocats100seams.png")
