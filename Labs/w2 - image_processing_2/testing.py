import pickle
from lab import *


def cl(l1, l2, row):
    width = l1["width"]
    row_start = row * width
    row_end = row_start + width
    p1 = l1["pixels"][row_start:row_end]
    p2 = l2["pixels"][row_start:row_end]
    return [[i, (x, y)] for i, (x, y) in enumerate(zip(p1, p2)) if x != y]


def cltotal(l1, l2):
    p1 = l1["pixels"]
    p2 = l2["pixels"]
    return [[i, (x, y)] for i, (x, y) in enumerate(zip(p1, p2)) if x != y]


def clpure(l1, l2):
    return [[i, (x, y)] for i, (x, y) in enumerate(zip(l1, l2)) if x != y]


row = 0


def pni(im1, im2):
    global row
    result = cl(im1, im2, row)
    row += 1
    return result


if __name__ == "__main__":
    smallfrog_energy = pickle.load(open("test_results/smallfrog_energy.pickle", "rb"))
    smallfrog_cem = pickle.load(
        open("test_results/smallfrog_cumulative_energy.pickle", "rb")
    )
    smallfrog_seam = pickle.load(
        open("test_results/smallfrog_minimum_energy_seam.pickle", "rb")
    )
    image = load_color_image("test_images/smallfrog.png")
    grey = greyscale_image_from_color_image(image)
    energy = compute_energy(grey)
    cem = cumulative_energy_map(energy)
    seam = minimum_energy_seam(cem)

    def pn():
        return pni(smallfrog_energy, energy)
