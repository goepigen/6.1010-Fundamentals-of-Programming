import time
from PIL import Image

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

def find_path(image, start_location, goal_color):
    safe_color = get_pixel(image, *start_location)
    path_color = (255, 230, 0)

    possible_paths = [[start_location]]
    visited = {start_location}

    width = get_width(image)
    height = get_height(image)

    set_pixel(image, *start_location, path_color)

    while possible_paths:
        current_path = possible_paths.pop(0)

        last_location = current_path[-1]
        for neighbor in get_neighbors(last_location, width, height):
            if (neighbor not in visited):
                neighbor_color = get_pixel(image, *neighbor)
                if neighbor_color == goal_color:
                    color_path(image, current_path)
                    return current_path
                elif neighbor_color == safe_color:
                    visited.add(neighbor)
                    set_pixel(image, *neighbor, path_color)
                    new_path = current_path[:]
                    new_path.append(neighbor)
                    possible_paths.append(new_path)
                
def color_path(image, path):
    for location in path:
        set_pixel(image, *location, (255, 0, 0))               

def get_neighbors(cell, width, height):
    row, col = cell

    potential_neighbors = [(row + 1,col), (row - 1,col), (row, col + 1), (row, col - 1)]
    return [ (nr, nc) for nr, nc in potential_neighbors if 0 <= nr < height and 0 <= nc < width]         

def is_same_color(color_1, color_2):
        return color_1[0] == color_2[0] and color_1[1] == color_2[1] and color_1[2] == color_2[2]

def flood_fill(image, location, new_color):
    """
    Given an image, replace the same-colored region around a given location
    with a given color.  Returns None but mutates the original image to
    reflect the change.

    Parameters:
      * image: the image to operate on
      * location: an (row, col) tuple representing the starting location of the
                  flood-fill process
      * new_color: the replacement color, as an (r, g, b) tuple where all values
                   are between 0 and 255, inclusive
    """
    print(f"You clicked at row {location[0]} col {location[1]}")

    original_color = get_pixel(image, *location)
    
    to_color = [location]
    visited = {location}
    
    set_pixel(image, *location, new_color)

    width = get_width(image)
    height = get_height(image)

    start = time.time()

    while to_color:
        this_cell = to_color.pop(0)

        for neighbor in get_neighbors(this_cell, width, height):
            neighbor_color = get_pixel(image, *neighbor)
            if (neighbor not in visited and is_same_color(neighbor_color, original_color)):
                set_pixel(image, *neighbor, new_color)
                to_color.append(neighbor)
                visited.add(neighbor)

    print(f'This took {time.time()-start} seconds')


##### IMAGE REPRESENTATION WITH SIMILAR ABSTRACTIONS TO LAB 1 AND 2


def get_width(image):
    return image.get_width() // SCALE

def get_height(image):
    return image.get_height() // SCALE


def get_pixel(image, row, col):
    # print(row, col)
    color = image.get_at((col * SCALE, row * SCALE))
    return (color.r, color.g, color.b)


def set_pixel(image, row, col, color):
    loc = row * SCALE, col * SCALE
    c = pygame.Color(*color)
    for i in range(SCALE):
        for j in range(SCALE):
            image.set_at((loc[1] + i, loc[0] + j), c)
    ## comment out the two lines below to avoid redrawing the image every time
    ## we set a pixel
    # screen.blit(image, (0, 0))
    # pygame.display.flip()


##### USER INTERFACE CODE
##### DISPLAY AN IMAGE AND CALL flood_fill WHEN THE IMAGE IS CLICKED

import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from pygame.locals import *

COLORS = {
    pygame.K_r: (255, 0, 0),
    pygame.K_w: (255, 255, 255),
    pygame.K_k: (0, 0, 0),
    pygame.K_g: (0, 255, 0),
    pygame.K_b: (0, 0, 255),
    pygame.K_c: (0, 255, 255),
    pygame.K_y: (255, 230, 0),
    pygame.K_p: (179, 0, 199),
    pygame.K_o: (255, 77, 0),
    pygame.K_n: (66, 52, 0),
    pygame.K_e: (152, 152, 152),
}

COLOR_NAMES = {
    pygame.K_r: "red",
    pygame.K_w: "white",
    pygame.K_k: "black",
    pygame.K_g: "green",
    pygame.K_b: "blue",
    pygame.K_c: "cyan",
    pygame.K_y: "yellow",
    pygame.K_p: "purple",
    pygame.K_o: "orange",
    pygame.K_n: "brown",
    pygame.K_e: "grey",
}

SCALE = 7
IMAGE = "huge_maze.png"

result = load_color_image(IMAGE)

{pixel for pixel in result["pixels"]}

pygame.init()
image = pygame.image.load(IMAGE)
dims = (image.get_width() * SCALE, image.get_height() * SCALE)
screen = pygame.display.set_mode(dims)
image = pygame.transform.scale(image, dims)
screen.blit(image, (0, 0))
pygame.display.flip()
initial_color = pygame.K_p
cur_color = COLORS[initial_color]
print("current color:", COLOR_NAMES[initial_color])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key in COLORS:
                cur_color = COLORS[event.key]
                print("current color:", COLOR_NAMES[event.key])
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            goal_color = (0, 255, 0)
            find_path(image, (event.pos[1] // SCALE, event.pos[0] // SCALE), goal_color)
            # flood_fill(image, (event.pos[1] // SCALE, event.pos[0] // SCALE), cur_color)
            screen.blit(image, (0, 0))
            pygame.display.flip()
