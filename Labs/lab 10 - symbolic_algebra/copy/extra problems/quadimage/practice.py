"""
6.1010 Fall 2022
Week 9 Optional Practice Exercises: QuadImage
"""

from PIL import Image

# no additional imports allowed!


class QuadImage:
    """
    Each instance of QuadImage has exactly 4 attributes:

    * width  : integer width of the image.
    * height : integer height of the image.
    * pixel  : None if there are no pixels in the quadrant or if the QuadImage
        has sub-quadrants. Otherwise, an int pixel value in the range [0, 255]
        signifying that all pixels in the quadrant have that value.
    * quadrants : if there are multiple pixels with different values,
        a list of four QuadImages which store the data for each sub-image in
        [top_left, top_right, bottom_left, bottom_right] order. Otherwise, an
        empty list.
    """

    def __init__(self, image_dict):
        """
        Given an image dictionary, convert it into a QuadImage.

        Parameters:
            * image_dict: an image dictionary of the form
            {
                'width'  : integer image width,
                'height' : integer image height,
                'pixels' : list of greyscale integer pixel values in
                           [0, 255] stored in row-major order.
            }
        """

        # initialize attributes
        self.width = image_dict["width"]
        self.height = image_dict["height"]
        self.pixel = None
        self.quadrants = []

        pixels = image_dict["pixels"]

        # if image contains no pixels, we have a blank QuadImage
        if not pixels:
            return

        # if all pixels in the image have the same value,
        # set pixel value
        if len(set(pixels)) == 1:
            self.pixel = pixels[0]
        else:
            # otherwise split image into four sub-images
            sub_images = split_image(image_dict)

            # make sub-quadrants
            for sub_image in sub_images:
                self.quadrants.append(QuadImage(sub_image))

    def __getitem__(self, point):
        """
        Given a (x, y) point inside the QuadImage,
        return the value associated with that pixel.
        """

        # TODO implement base case

        # Recursive case: search sub-quadrants for value
        split_x = self.quadrants[0].width
        split_y = self.quadrants[0].height

        # find which quadrant the point is in,
        # and update the point to fit in quadrant
        quad_index = 0

        # point is in top right quadrant
        if point[0] >= split_x and point[1] < split_y:
            quad_index = 1
            point = (point[0] - split_x, point[1])

        # TODO update point / quad_index for other quadrants

        # TODO get pixel value for point in quadrant

    def __iter__(self):
        """
        Iter generates all pixels in the QuadImage and outputs them
        in any order in the form (x, y, pixel_value).

        Note: this method should not use __getitem__.
        """

        if self.width == 0 and self.height == 0:
            return  # base case: empty quadrant, nothing to yield

        # what is the other base case? what should we yield in that case?

        # else yield adjusted pixel points and values for each sub-quadrant


def split_image(image_dict):
    """
    Splits an image dictionary into four roughly equal sized
    image dictionaries. This function has been provided for
    should not be modified. image_dict must contain at least
    1 pixel.

    Parameters:
        * image_dict: an image dictionary of the form
            {
                'width'  : integer image width,
                'height' : integer image height,
                'pixels' : list of greyscale integer pixel values in
                           [0, 255] stored in row-major order.
            }

    Returns:
        A list containing four sub-image dictionaries, in the order of
        [top_left, top_right, bottom_left, bottom_right]
        that when combined form the original image.
        Sub-images may have 0 pixel values.

    """
    # check that image contains at least one pixel
    assert (
        image_dict["width"] > 0
        and image_dict["height"] > 0
        and len(image_dict["pixels"]) > 1
    ), f"Empty image dict! {image_dict}"

    # find midpoints to split image on
    split_x = image_dict["width"] // 2
    split_x += 0 if image_dict["width"] % 2 == 0 else 1
    split_y = image_dict["height"] // 2
    split_y += 0 if image_dict["height"] % 2 == 0 else 1

    # initialize four sub-images
    sub_images = []
    for h in [split_y, (image_dict["height"] - split_y)]:
        for w in [split_x, (image_dict["width"] - split_x)]:
            if w == 0 or h == 0:
                sub_images.append({"height": 0, "width": 0, "pixels": []})
            else:
                sub_images.append({"height": h, "width": w, "pixels": []})

    i = 0  # iterate through pixels in row major order
    for y in range(image_dict["height"]):
        for x in range(image_dict["width"]):
            # sort each pixel location into proper sub_image
            quad_index = 3  # bottom right quadrant
            if x < split_x and y < split_y:
                quad_index = 0  # top left
            elif x >= split_x and y < split_y:
                quad_index = 1  # top right
            elif x < split_x and y >= split_y:
                quad_index = 2  # bottom left

            sub_images[quad_index]["pixels"].append(image_dict["pixels"][i])
            i += 1

    return sub_images


def load_image(filename):
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
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2])
                for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        w, h = img.size
        return {"width": h, "height": w, "pixels": pixels}


if __name__ == "__main__":
    # Example: load image -> convert to QuadImage
    # square = load_image('resources/square.png')
    # quad = QuadImage(square)

    # Your code here:
    pass
