#!/usr/bin/env python3
"""
6.101 Lab:
Mice-sleeper
"""

# import typing  # optional import
# import pprint  # optional import
import doctest

from debug_recursion import show_recursive_structure

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game, all_keys=False):
    """
    Prints a human-readable version of a game (provided as a dictionary)

    By default uses only "board", "dimensions", "state", "visible" keys (used
    by doctests). Setting all_keys=True shows all game keys.
    """
    if all_keys:
        keys = sorted(game)
    else:
        keys = ("board", "dimensions", "state", "visible")
        # Use only default game keys. If you modify this you will need
        # to update the docstrings in other functions!

    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# HELPERS


def get_2d_neighbors(r, c, nrows, ncols):
    """
    Given the position of a cell (row r and column c) and given dimensions of a 2d grid (nrows x ncols), returns
    the positions of the adjacent cells in the grid.

    >>> get_2d_neighbors(0, 0, 2, 2)
    [(0, 1), (1, 0), (1, 1)]
    """
    return get_neighbors_nd((r, c), (nrows, ncols))


def check_victory(game):
    """
    Returns True if the game is in a "won" state, False otherwise.
    """
    return check_victory_nd(game)


# 2-D IMPLEMENTATION

MOUSE = "m"


def new_game_2d(nrows, ncols, mouse_locations):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mice (list): List of mouse locations as (row, column) tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    return new_game_nd((nrows, ncols), mouse_locations)


def reveal_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mice (including diagonally), then recursively reveal its eight
    neighbors.  Return an integer indicating how many new squares were revealed
    in total, including neighbors, and neighbors of neighbors, and so on.

    The state of the game should be changed to 'lost' when at least one mouse
    is visible on the board, 'won' when all safe squares (squares that do not
    contain a mouse) and no mice are visible, and 'ongoing' otherwise.

    If the game is not ongoing, or if the given square has already been
    revealed, reveal_2d should not reveal any squares.

    Parameters:
       game (dict): Game state
       row (int): Where to start revealing cells (row)
       col (int): Where to start revealing cells (col)

    Returns:
       int: the number of new squares revealed

    >>> game = new_game_2d(2, 4, [(0,0), (1, 0), (1, 1)])
    >>> reveal_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, True, True]
        [False, False, True, True]
    >>> reveal_2d(game, 0, 1)
    1
    >>> dump(game)
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2, 4)
    state: won
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = new_game_2d(2, 4, [(0,0), (1, 0), (1, 1)])  # restart game
    >>> reveal_2d(game, 0, 3)
    4
    >>> reveal_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['m', 3, 1, 0]
        ['m', 'm', 1, 0]
    dimensions: (2, 4)
    state: lost
    visible:
        [True, False, True, True]
        [False, False, True, True]
    """
    return reveal_nd(game, (row, col))


def render_2d(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    'm' (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mice).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored and
    all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = new_game_2d(2, 4, [(0,0), (1, 0), (1, 1)])
    >>> render_2d(game, False)
    [['_', '_', '_', '_'], ['_', '_', '_', '_']]
    >>> render_2d(game, True)
    [['m', '3', '1', ' '], ['m', 'm', '1', ' ']]
    >>> reveal_2d(game, 0, 3)
    4
    >>> render_2d(game, False)
    [['_', '_', '1', ' '], ['_', '_', '1', ' ']]
    """
    if all_visible:
        return [[" " if el == 0 else str(el) for el in row] for row in game["board"]]

    result = [
        [
            (
                (" " if game["board"][r][c] == 0 else str(game["board"][r][c]))
                if game["visible"][r][c]
                else ("_" if (r, c) not in game["bed locations"] else "B")
            )
            for c in range(game["dimensions"][1])
        ]
        for r in range(game["dimensions"][0])
    ]

    return result


def toggle_bed_2d(game, row, col):
    """
    Place a visual marker representing a bed at position (row, col) on the board.

    Args:
        game: an instance of the game
        row: int
        col: int
    """
    return toggle_bed_nd(game, (row, col))


# HELPERS N-D


def get_neighbors_nd(pos, dim):
    """
    Get the neighbors of cell on the board at position pos taking into
    account the dimensions of the board in dim.

    Note that the cell at position pos is not a neighbor.

    Args:
        pos: a position in the n-dimensional board

        dim: tuple with length equal to the number of dimensions of the
        board and each element equal to thesize of the corresponding dimension.

    Returns a list of tuples, each tuple being the position of a neighbor.
    """
    # base case: all dimensions except the first in the original dim variable are removed
    # e.g. if original call had pos = (5, 13, 0) and dim = (10, 20, 3), then we reach the base case of
    # pos = (5) and dim = (10) and the returned list is [(4), (6)]
    if len(dim) == 1:
        return [(pos[0] + i,) for i in [-1, 1] if 0 <= pos[0] + i < dim[0]]

    # recurse removing the last dimension
    # ie get neighbors of pos[:-1], a smaller problem.
    subneighbors = get_neighbors_nd(pos[:-1], dim[:-1])

    # Obtain neighbors of subneighbors by adding new dimension to the latter.
    # Since the latter don't include pos[:-1] (because it is not a neighbor of itself), we obtain
    # the neighbors of pos using a second list, which adds [-1, 1] to the last dimension of pos
    # we don't add 0 because this would simply give pos as a neighbor of itself.
    return [
        (*pn, pos[-1] + i)
        for i in [-1, 0, 1]
        for pn in subneighbors
        if 0 <= pos[-1] + i < dim[-1]
    ] + [(*pos[:-1], pos[-1] + i) for i in [-1, 1] if 0 <= pos[-1] + i < dim[-1]]


def make_ndim_array(dim, initial_val=0):
    """
    Creates an n-dimensional array populated with initial values initial_val.

    Args:
        dim: n-tuple with the length of each dimension
        initial_val: int or str

    Returns an n-dim array (as a nested list structure)
    """
    if len(dim) == 1:
        return dim[0] * [initial_val]

    return [make_ndim_array(dim[1:], initial_val) for _ in range(dim[0])]


def set_val_at_board_pos(board, pos, val):
    """
    Given an n-dimensional nested list, set the value at pos to val.
    Args:
        board: n-dimensional nested list
        pos: n-tuple
        val: int or str
    Returns
        Mutated board.
    """
    ref = board
    for p in pos[:-1]:
        ref = ref[p]
    ref[pos[-1]] = val


def get_val_at_board_pos(board, pos):
    """
    Given an n-dimensional nested list, get the value at pos.
    Args:
        board: n-dimensional nested list
        pos: n-tuple
    Returns
        value at pos.
    """
    ref = board
    for p in pos:
        ref = ref[p]
    return ref


def all_coords(dim):
    """
    Given an n-tuple representing the size of each dimension of an n-dimensional array,
    return all the possible positions in the array.
    Args
        dim: n-tuple of positive ints
    Returns
        list of n-tuples, where each n-tuple is a position.
    """
    if len(dim) == 1:
        return [(p,) for p in range(dim[0])]

    sub_coords = all_coords(dim[1:])

    return [(p, *sc) for sc in sub_coords for p in range(dim[0])]


def check_victory_nd(game):
    """
    Returns True if the game is in a "won" state, False otherwise.
    """
    dim = game["dimensions"]
    return all(
        [
            (
                not get_val_at_board_pos(game["visible"], pos)
                if pos in game["mouse locations"]
                else get_val_at_board_pos(game["visible"], pos)
            )
            for pos in all_coords(dim)
        ]
    )


# N-D IMPLEMENTATION


def make_board(dimensions, mouse_locations):
    """
    Creates an n-dimensional array and populates the array based on mouse_locations.
    Locations in mouse_locations are populated with the value of the variable MOUSE.
    All other locations contain a number that is computed based on the number of mice
    locations around it.
    Args
        dimensions: n-tuple of ints
        mouse_locations: list of n-tuples representing positions in the n-dim array
    Returns
        n-dim array representing the board
    """
    board = make_ndim_array(dimensions)
    for pos in mouse_locations:
        set_val_at_board_pos(board, pos, MOUSE)

    for pos in mouse_locations:
        neighbors = get_neighbors_nd(pos, dimensions)
        for n_pos in neighbors:
            val = get_val_at_board_pos(board, n_pos)
            if val != MOUSE:
                set_val_at_board_pos(board, n_pos, val + 1)
    return board


def new_game_nd(dimensions, mouse_locations):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       dimensions (tuple): Dimensions of the board
       mice (list): mouse locations as a list of tuples, each an
                    N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, 'm'], [3, 3], [1, 1], [0, 0]]
        [['m', 3], [3, 'm'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """
    board = make_board(dimensions, mouse_locations)

    return {
        "dimensions": dimensions,
        "board": board,
        "state": "ongoing",
        "visible": make_ndim_array(dimensions, False),
        "mouse locations": set(mouse_locations),
        "first move": True,
        "bed locations": set(),
    }


def reveal_nd(game, pos):
    """
    Recursively reveal square at coords and neighboring squares.

    Update the visible to reveal square at the given coordinates; then
    recursively reveal its neighbors, as long as coords does not contain and is
    not adjacent to a mouse.  Return a number indicating how many squares were
    revealed.  No action should be taken (and 0 should be returned) if the
    incoming state of the game is not 'ongoing', or if the given square has
    already been revealed.

    The updated state is 'lost' when at least one mouse is visible on the
    board, 'won' when all safe squares (squares that do not contain a mouse)
    and no mice are visible, and 'ongoing' otherwise.

    Parameters:
       coordinates (tuple): Where to start revealing squares

    Returns:
       int: number of squares revealed

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, 'm'], [3, 3], [1, 1], [0, 0]]
        [['m', 3], [3, 'm'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> reveal_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, 'm'], [3, 3], [1, 1], [0, 0]]
        [['m', 3], [3, 'm'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: lost
    visible:
        [[False, True], [False, False], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    """

    if pos in game["bed locations"]:
        return 0

    if game["first move"]:
        game["first move"] = False
        val = get_val_at_board_pos(game["board"], pos)
        if val != 0:
            relocate = []
            if val == MOUSE:
                relocate.append(pos)
            neighbors = set(get_neighbors_nd(pos, game["dimensions"]))
            relocate.extend(list(neighbors & game["mouse locations"]))
            gen_random_pos = random_coordinates(game["dimensions"])
            while relocate:
                random = next(gen_random_pos)
                if random not in game["mouse locations"] | neighbors | {pos}:
                    m_pos = relocate.pop()
                    game["mouse locations"].remove(m_pos)
                    game["mouse locations"].add(random)
            game["board"] = make_board(game["dimensions"], game["mouse locations"])

    if game["state"] != "ongoing":
        return 0

    visited = set()

    def reveal_rec(pos):
        if pos in visited:
            return 0

        visited.add(pos)

        if pos in game["bed locations"]:
            return 0

        if get_val_at_board_pos(game["visible"], pos):
            return 0

        set_val_at_board_pos(game["visible"], pos, True)
        revealed = 1

        val = get_val_at_board_pos(game["board"], pos)
        if val == MOUSE:
            game["state"] = "lost"
            return revealed

        if val == 0:
            neighbors = get_neighbors_nd(pos, game["dimensions"])
            for n_pos in neighbors:
                revealed += reveal_rec(n_pos)

        return revealed

    revealed = reveal_rec(pos)

    if check_victory_nd(game):
        game["state"] = "won"

    return revealed


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), 'm'
    (mice), ' ' (empty squares), or '1', '2', etc. (squares neighboring mice).
    The game['visible'] array indicates which squares should be visible.  If
    all_visible is True (the default is False), the game['visible'] array is
    ignored and all cells are shown.

    Parameters:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> reveal_nd(g, (0, 3, 0))
    8
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', 'm'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['m', '3'], ['3', 'm'], ['1', '1'], [' ', ' ']]]
    """
    dim = game["dimensions"]

    rendered = make_ndim_array(dim, "_")

    all_positions = all_coords(dim)

    if all_visible:
        for pos in all_positions:
            val = get_val_at_board_pos(game["board"], pos)
            set_val_at_board_pos(rendered, pos, " " if val == 0 else str(val))
        return rendered

    for pos in all_positions:
        if pos in game["bed locations"]:
            set_val_at_board_pos(rendered, pos, "B")
            continue
        val = get_val_at_board_pos(game["board"], pos)
        visible = get_val_at_board_pos(game["visible"], pos)
        if visible:
            if val == 0:
                set_val_at_board_pos(rendered, pos, " ")
            else:
                set_val_at_board_pos(rendered, pos, str(val))
    return rendered


def toggle_bed_nd(game, coords):
    """
    Place a visual marker representing a bed at position represented by coords on the board.

    Args:
        game: an instance of the game
        coords: n-tuple of coordinates on the board
    """
    if get_val_at_board_pos(game["visible"], coords) or game["state"] != "ongoing":
        return None

    if coords in game["bed locations"]:
        game["bed locations"].remove(coords)
        return False

    game["bed locations"].add(coords)
    return True


def random_coordinates(dimensions):
    """
    Given a tuple representing the dimensions of a game board, return an
    infinite generator that yields pseudo-random coordinates within the board.
    For a given tuple of dimensions, the output sequence will always be the
    same.
    """

    def prng(state):
        # see https://en.wikipedia.org/wiki/Lehmer_random_number_generator
        while True:
            yield (state := state * 48271 % 0x7FFFFFFF) / 0x7FFFFFFF

    prng_gen = prng(sum(dimensions) + 61016101)
    for _ in zip(range(1), prng_gen):
        pass
    while True:
        yield tuple(int(dim * val) for val, dim in zip(prng_gen, dimensions))


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so,
    # comment out the above line, and uncomment the below line of code.  This
    # may be useful as you write/debug individual doctests or functions.  Also,
    # the verbose flag can be set to True to see all test results, including
    # those that pass.
    #
    # doctest.run_docstring_examples(
    #    render_2d,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
    game = new_game_2d(8, 8, [(6, 6), (6, 1)])
    result = reveal_2d(game, 6, 7)
