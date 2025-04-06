#!/usr/bin/env python3

import os
import pickle
import hashlib

import lab
import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


def compare_images(im1, im2):
    assert set(im1.keys()) == {
        "height",
        "width",
        "pixels",
    }, "Incorrect keys in dictionary"
    assert im1["height"] == im2["height"], "Heights must match"
    assert im1["width"] == im2["width"], "Widths must match"
    assert (
        len(im1["pixels"]) == im1["height"] * im1["width"]
    ), "Incorrect number of pixels"
    assert all(isinstance(i, int) for i in im1["pixels"]), "Pixels must all be integers"
    assert all(
        0 <= i <= 255 for i in im1["pixels"]
    ), "Pixels must all be in the range from [0, 255]"
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1["pixels"], im2["pixels"])):
        if i != j:
            pix_incorrect = (ix, abs(i - j))
    assert pix_incorrect == (None, None), (
        "Pixels must match.  Incorrect value at location %s (differs from expected by %s)"
        % pix_incorrect
    )


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


def test_correlated_identity_zero():
    im = lab.load_greyscale_image(
        os.path.join(TEST_DIRECTORY, "test_images", "centered_pixel.png")
    )

    kernel = {"size": 3, "weights": [0, 0, 0, 0, 1, 0, 0, 0, 0]}

    result = lab.correlate(im, kernel, "zero")
    expected = im
    compare_images(result, expected)


def test_correlated_translate_zero():
    im = lab.load_greyscale_image(
        os.path.join(TEST_DIRECTORY, "test_images", "centered_pixel.png")
    )

    kernel = {"size": 3, "weights": [0, 0, 0, 1, 0, 0, 0, 0, 0]}

    result = lab.correlate(im, kernel, "zero")
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [0 for i in range(61)] + [255] + [0 for i in range(61)],
    }
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


if __name__ == "__main__":
    import sys

    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
