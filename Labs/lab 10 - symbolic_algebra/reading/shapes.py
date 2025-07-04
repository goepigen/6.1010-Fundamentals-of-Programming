## FRONT MATTER FOR DRAWING/SAVING IMAGES, ETC

from PIL import Image as PILImage

# some test colors
COLORS = {
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "green": (0, 100, 0),
    "lime": (0, 255, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "yellow": (255, 230, 0),
    "purple": (179, 0, 199),
    "pink": (255, 0, 255),
    "orange": (255, 77, 0),
    "brown": (66, 52, 0),
    "grey": (152, 152, 152),
}


def new_image(width, height, fill=(240, 240, 240)):
    return {
        "height": height,
        "width": width,
        "pixels": [fill for r in range(height) for c in range(width)],
    }


def flat_index(image, x, y):
    assert 0 <= x < image["width"] and 0 <= y < image["height"]
    return (image["height"] - 1 - y) * image["width"] + x


def get_pixel(image, x, y):
    return image["pixels"][flat_index(image, x, y)]


def set_pixel(image, x, y, c):
    assert (
        isinstance(c, tuple)
        and len(c) == 3
        and all((isinstance(i, int) and 0 <= i <= 255) for i in c)
    )
    if 0 <= x < image["width"] and 0 <= y < image["height"]:
        image["pixels"][flat_index(image, x, y)] = c


def save_color_image(image, filename, mode="PNG"):
    out = PILImage.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


## SHAPES!


class Shape:
    # All subclasses MUST implement the following:
    #
    # __contains__(self, p) returns True if point p is inside the shape
    # represented by self
    #
    # note that "(x, y) in s" for some instance of Shape
    # will be translated automatically to "s.__contains__((x, y))"
    #
    # s.center should give the (x,y) center point of the shape
    #
    # draw(self, image, color) should mutate the given image to draw the shape
    # represented by self on the given image in the given color
    #
    def __contains__(self, p):
        raise NotImplementedError("Subclass of Shape did not define __contains__")

    def draw(self, image, color):
        for x in range(image["width"]):
            for y in range(image["height"]):
                if (x, y) in self:
                    set_pixel(image, x, y, color)

    def _combine(self, other, combiner_cls):
        if isinstance(other, list):
            if all(isinstance(s, Shape) for s in other):
                return combiner_cls([self] + other)
        if isinstance(other, Shape):
            return combiner_cls([self, other])
        raise TypeError("Argument should be a Shape or a list of Shapes.")

    def __or__(self, other):
        return self._combine(other, ShapeUnion)

    def __and__(self, other):
        return self._combine(other, ShapeIntersection)

    def __sub__(self, other):
        if not isinstance(other, Shape):
            raise TypeError("Subtrahend must be a Shape.")
        return ShapeDifference(self, other)


# BASIC SHAPES
class Triangle(Shape):
    def __init__(self, vertices):
        assert len(vertices) == 3, "Triangle must have exactly 3 vertices"
        self.vertices = vertices

    def __contains__(self, p):
        def area(p1, p2, p3):
            # Absolute value of the signed area (shoelace formula)
            return abs(
                (
                    p1[0] * (p2[1] - p3[1])
                    + p2[0] * (p3[1] - p1[1])
                    + p3[0] * (p1[1] - p2[1])
                )
                / 2
            )

        A, B, C = self.vertices
        total_area = area(A, B, C)
        area1 = area(p, B, C)
        area2 = area(A, p, C)
        area3 = area(A, B, p)

        return (
            abs(total_area - (area1 + area2 + area3)) < 1e-5
        )  # Tolerance for float errors


class Circle(Shape):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __contains__(self, p):
        return (
            sum(
                [
                    (coord_p - coord_center) ** 2
                    for coord_p, coord_center in zip(p, self.center)
                ]
            )
            <= self.radius**2
        )


class Rectangle(Shape):
    def __init__(self, lower_left, height, width):
        self.lower_left = lower_left
        self.height = height
        self.width = width

    @property
    def center(self):
        return (
            self.lower_left[0] + self.width // 2,
            self.lower_left[1] + self.height // 2,
        )

    def __contains__(self, p):
        px, py = p
        llx, lly = self.lower_left

        return llx <= px <= llx + self.width and lly <= py <= lly + self.height


class Square(Rectangle):
    def __init__(self, lower_left, side_length):
        Rectangle.__init__(self, lower_left, side_length, side_length)


# COMBINATIONS


class Combination(Shape):
    def __init__(self, shapes):
        self.shapes = shapes


class ShapeUnion(Combination):

    def __contains__(self, p):
        return any([p in shape for shape in self.shapes])


class ShapeDifference(Shape):
    def __init__(self, minuend, subtrahend):
        self.minuend = minuend
        self.subtrahend = subtrahend

    def __contains__(self, p):
        return p in self.minuend and p not in self.subtrahend


class ShapeIntersection(Combination):

    def __contains__(self, p):
        return all([p in shape for shape in self.shapes])


if __name__ == "__main__":
    out_image = new_image(500, 500)

    # add code here to draw some shapes
    small_circle = Circle((450, 450), 50)
    big_circle = Circle((250, 250), 100)
    small_rectangle = Rectangle((90, 90), 50, 50)
    big_rectangle = Rectangle((100, 100), 100, 100)
    big_triangle = Triangle([(10, 400), (250, 450), (0, 10)])
    union = small_circle | small_rectangle
    intersection = big_circle & big_rectangle
    difference = big_circle - big_rectangle
    shapes = [
        (
            ShapeIntersection([big_circle, big_rectangle]),
            COLORS["blue"],
        ),
        (union, COLORS["green"]),
        (intersection, COLORS["lime"]),
        (difference, COLORS["orange"]),
        (big_triangle, COLORS["purple"]),
    ]
    for shape, color in shapes:
        shape.draw(out_image, color)
    save_color_image(out_image, "test1.png")
