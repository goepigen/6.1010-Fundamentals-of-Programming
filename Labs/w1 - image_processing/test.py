#!/usr/bin/env python3

import os
import pickle
import hashlib

import lab
import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


def compare_images(result, expected):
    assert set(result.keys()) == {
        "height",
        "width",
        "pixels",
    }, f"Incorrect keys in dictionary"
    assert result["height"] == expected["height"], "Heights must match"
    assert result["width"] == expected["width"], "Widths must match"
    assert (
        len(result["pixels"]) == result["height"] * result["width"]
    ), f"Incorrect number of pixels, expected {result['height']*result['width']}"
    num_incorrect_val = 0
    first_incorrect_val = None
    num_bad_type = 0
    first_bad_type = None
    num_bad_range = 0
    first_bad_range = None

    row, col = 0, 0
    correct_image = True
    for index, (res, exp) in enumerate(zip(result["pixels"], expected["pixels"])):
        if not isinstance(res, int):
            correct_image = False
            num_bad_type += 1
            if not first_bad_type:
                first_bad_type = f"Pixels must all be integers!"
                first_bad_type += (
                    f"\nPixel had value {res} at index {index} (row {row}, col {col})."
                )
        if res < 0 or res > 255:
            num_bad_range += 1
            correct_image = False
            if not first_bad_range:
                first_bad_range = f"Pixels must all be in the range from [0, 255]!"
                first_bad_range += (
                    f"\nPixel had value {res} at index {index} (row {row}, col {col})."
                )
        if res != exp:
            correct_image = False
            num_incorrect_val += 1
            if not first_incorrect_val:
                first_incorrect_val = f"Pixels must match"
                first_incorrect_val += f"\nPixel had value {res} but expected {exp} at index {index} (row {row}, col {col})."

        if col + 1 == result["width"]:
            col = 0
            row += 1
        else:
            col += 1

    msg = "Image is correct!"
    if first_bad_type:
        msg = (
            first_bad_type
            + f"\n{num_bad_type} pixel{'s'*int(num_bad_type>1)} had this problem."
        )
    elif first_bad_range:
        msg = (
            first_bad_range
            + f"\n{num_bad_range} pixel{'s'*int(num_bad_range>1)} had this problem."
        )
    elif first_incorrect_val:
        msg = (
            first_incorrect_val
            + f"\n{num_incorrect_val} pixel{'s'*int(num_incorrect_val>1)} had incorrect value{'s'*int(num_incorrect_val>1)}."
        )

    assert correct_image, msg


def test_load():
    result = lab.load_greyscale_image(
        os.path.join(TEST_DIRECTORY, "test_images", "centered_pixel.png")
    )
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            255,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
    }
    compare_images(result, expected)


def test_my_inverted():
    im = {"height": 1, "width": 4, "pixels": [0, 74, 136, 195]}

    expected = {"height": 1, "width": 4, "pixels": [255, 181, 119, 60]}

    assert lab.inverted(im) == expected, "Inverted image not as expected."


def test_inverted_1():
    im = lab.load_greyscale_image(
        os.path.join(TEST_DIRECTORY, "test_images", "centered_pixel.png")
    )
    result = lab.inverted(im)
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [255 for i in range(60)] + [0] + [255 for i in range(60)],
    }
    compare_images(result, expected)


def test_inverted_2():
    image = {"height": 1, "width": 4, "pixels": [12, 71, 150, 217]}

    expected = {"height": 1, "width": 4, "pixels": [243, 184, 105, 38]}

    result = lab.inverted(image)
    compare_images(result, expected)


@pytest.mark.parametrize("fname", ["mushroom", "twocats", "chess"])
def test_inverted_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", "%s.png" % fname)
    expfile = os.path.join(TEST_DIRECTORY, "test_results", "%s_invert.png" % fname)
    im = lab.load_greyscale_image(inpfile)
    oim = object_hash(im)
    result = lab.inverted(im)
    expected = lab.load_greyscale_image(expfile)
    assert object_hash(im) == oim, "Be careful not to modify the original image!"
    compare_images(result, expected)


@pytest.mark.parametrize("kernsize", [1, 3, 7])
@pytest.mark.parametrize("fname", ["mushroom", "twocats", "chess"])
def test_blurred_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", "%s.png" % fname)
    expfile = os.path.join(
        TEST_DIRECTORY, "test_results", "%s_blur_%02d.png" % (fname, kernsize)
    )
    input_img = lab.load_greyscale_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.blurred(input_img, kernsize)
    expected = lab.load_greyscale_image(expfile)
    assert (
        object_hash(input_img) == input_hash
    ), "Be careful not to modify the original image!"
    compare_images(result, expected)


def test_blurred_black_image():
    image = {"height": 6, "width": 5, "pixels": [255 for i in range(30)]}

    kernel1 = lab.box_blur_kernel(5)
    kernel2 = lab.box_blur_kernel(10)

    result1 = lab.blurred(image, kernel1["size"])
    result2 = lab.blurred(image, kernel2["size"])

    expected = image

    compare_images(result1, expected)
    compare_images(result2, expected)


def test_blurred_centered_pixel():
    image = lab.load_greyscale_image(
        os.path.join(TEST_DIRECTORY, "test_images", "centered_pixel.png")
    )

    kernel1 = lab.box_blur_kernel(5)
    kernel2 = lab.box_blur_kernel(11)

    result1 = lab.blurred(image, kernel1["size"])
    result2 = lab.blurred(image, kernel2["size"])

    expected1 = {
        "height": 11,
        "width": 11,
        "pixels": [0 for i in range(33)]
        + [0 for i in range(3)]
        + [round(255 / 25) for i in range(5)]
        + [0 for i in range(3)]
        + [0 for i in range(3)]
        + [round(255 / 25) for i in range(5)]
        + [0 for i in range(3)]
        + [0 for i in range(3)]
        + [round(255 / 25) for i in range(5)]
        + [0 for i in range(3)]
        + [0 for i in range(3)]
        + [round(255 / 25) for i in range(5)]
        + [0 for i in range(3)]
        + [0 for i in range(3)]
        + [round(255 / 25) for i in range(5)]
        + [0 for i in range(3)]
        + [0 for i in range(33)],
    }

    expected2 = {
        "height": 11,
        "width": 11,
        "pixels": [round(255 / 121) for i in range(121)],
    }

    compare_images(result1, expected1)
    compare_images(result2, expected2)


@pytest.mark.parametrize("kernsize", [1, 3, 9])
@pytest.mark.parametrize("fname", ["mushroom", "twocats", "chess"])
def test_sharpened_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", "%s.png" % fname)
    expfile = os.path.join(
        TEST_DIRECTORY, "test_results", "%s_sharp_%02d.png" % (fname, kernsize)
    )
    input_img = lab.load_greyscale_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.sharpened(input_img, kernsize)
    expected = lab.load_greyscale_image(expfile)
    assert (
        object_hash(input_img) == input_hash
    ), "Be careful not to modify the original image!"
    compare_images(result, expected)


@pytest.mark.parametrize("fname", ["mushroom", "twocats", "chess"])
def test_edges_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", "%s.png" % fname)
    expfile = os.path.join(TEST_DIRECTORY, "test_results", "%s_edges.png" % fname)
    input_img = lab.load_greyscale_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.edges(input_img)
    expected = lab.load_greyscale_image(expfile)
    assert (
        object_hash(input_img) == input_hash
    ), "Be careful not to modify the original image!"
    compare_images(result, expected)


def test_edges_centered_pixel():
    image = lab.load_greyscale_image(
        os.path.join(TEST_DIRECTORY, "test_images", "centered_pixel.png")
    )

    expected = {
        "height": 11,
        "width": 11,
        "pixels": [0 for i in range(44)]
        + [0 for i in range(4)]
        + [255 for i in range(3)]
        + [0 for i in range(4)]
        + [0 for i in range(4)]
        + [255, 0, 255]
        + [0 for i in range(4)]
        + [0 for i in range(4)]
        + [255 for i in range(3)]
        + [0 for i in range(4)]
        + [0 for i in range(44)],
    }
    result = lab.edges(image)
    compare_images(result, expected)
