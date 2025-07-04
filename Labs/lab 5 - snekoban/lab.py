"""
6.1010 Lab:
Snekoban Game
"""

# import json # optional import for loading test_levels
# import typing # optional import
# import pprint # optional import

# NO ADDITIONAL IMPORTS!

DIRECTION_VECTOR = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def make_new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    height = len(level_description)
    width = len(level_description[0])

    game = {
        "params": {
            "width": width,
            "height": height,
            "wall": set(),
            "target": set(),
        },
        "state": {"computer": set(), "player position": None},
    }

    for row_i, _ in enumerate(level_description):
        for col_j, __ in enumerate(level_description[row_i]):
            position = (row_i, col_j)
            objs = level_description[row_i][col_j]

            for obj in objs:
                if obj == "wall":
                    game["params"]["wall"].add(position)
                elif obj == "target":
                    game["params"]["target"].add(position)
                elif obj == "computer":
                    game["state"]["computer"].add(position)
                elif obj == "player":
                    game["state"]["player position"] = position
    return {
        "params": {
            "width": width,
            "height": height,
            "wall": frozenset(game["params"]["wall"]),
            "target": frozenset(game["params"]["target"]),
        },
        "state": game["state"],
    }


def victory_check(game):
    """
    Given a game representation (of the form returned from make_new_game),
    return a Boolean: True if the given game satisfies the victory condition,
    and False otherwise.
    """
    if not game["params"]["target"] or not game["state"]["computer"]:
        return False

    return game["params"]["target"] == game["state"]["computer"]


def step_game(game, direction):
    """
    Given a game representation (of the form returned from make_new_game),
    return a game representation (of that same form), representing the
    updated game after running one step of the game.  The user's input is given
    by direction, which is one of the following:
        {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    player_pos = game["state"]["player position"]

    adjacent_pos = tuple(
        (v1 + v2 for v1, v2 in zip(player_pos, DIRECTION_VECTOR[direction]))
    )

    # If adjacent position is a wall, do nothing and return None.
    if adjacent_pos in game["params"]["wall"]:
        return game

    new_game = {
        "params": game["params"],
        "state": {
            "player position": game["state"]["player position"],
            "computer": set(game["state"]["computer"]),
        },
    }

    # Get the objects in the adjacent position ("target, computer, wall")

    adjacent_pos_is_empty = is_position_empty(game, adjacent_pos)

    # If adjacent position is a computer
    if adjacent_pos in game["state"]["computer"]:
        # get the adjacent to the computer position
        computer_adjacent_pos = tuple(
            (v1 + v2 for v1, v2 in zip(adjacent_pos, DIRECTION_VECTOR[direction]))
        )
        # if the adjacent position to the computer contains a wall or another computer, do
        # nothing and return.
        if (
            computer_adjacent_pos in new_game["params"]["wall"]
            or computer_adjacent_pos in new_game["state"]["computer"]
        ):
            return game
        # if the adjacent position to the computer position is empty or contains a target (and
        # since we've already checked for a computer in this position we know the target is by
        # itself) then move the player, move the computer, and return.
        computer_adjacent_pos_is_empty = is_position_empty(game, computer_adjacent_pos)
        if (
            computer_adjacent_pos_is_empty
            or computer_adjacent_pos in new_game["params"]["target"]
        ):
            new_game["state"]["player position"] = adjacent_pos
            # move the computer
            new_game["state"]["computer"].remove(adjacent_pos)
            new_game["state"]["computer"].add(computer_adjacent_pos)
            return new_game
    # If adjacent position is a target (note that we know at this point that there is no computer
    # in this position), move the player to the adjacent position.
    elif adjacent_pos in game["params"]["target"] or adjacent_pos_is_empty:
        new_game["state"]["player position"] = adjacent_pos
        return new_game


def is_position_empty(game, pos):
    return (
        pos not in game["params"]["wall"]
        and pos not in game["state"]["computer"]
        and pos not in game["params"]["target"]
        and pos not in game["state"]["player position"]
    )


def dump_game(game):
    """
    Given a game representation (of the form returned from make_new_game),
    convert it back into a level description that would be a suitable input to
    make_new_game (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """

    width = game["params"]["width"]
    height = game["params"]["height"]

    level_representation = [[[] for i in range(width)] for j in range(height)]

    for k, v in game.items():
        if k == "params":
            for k1, v1 in v.items():
                if k1 in ["width", "height"]:
                    continue
                if k1 in ["wall", "target"]:
                    for pos in v1:
                        level_representation[pos[0]][pos[1]].append(k1)

        if k == "state":
            for k1, v1 in v.items():
                if k1 == "player position":
                    level_representation[v1[0]][v1[1]].append("player")
                if k1 == "computer":
                    for pos in v1:
                        level_representation[pos[0]][pos[1]].append(k1)

    return level_representation


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from make_new_game), find
    a solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """

    state_path = find_path(get_neighbor_states, game, victory_check)

    if state_path is None:
        return None

    return compute_moves_from_path(state_path)


# HELPERS


def get_full_state(state, game_params):
    return {
        **game_params,
        "player position": state[1],
        "computer": set(state[2]),
    }


def get_neighbor_states(game):
    neighbor_states = []
    for direction in DIRECTION_VECTOR:
        neighbor_game = step_game(game, direction)
        if neighbor_game == game:
            continue
        neighbor_state = neighbor_game["state"]
        neighbor_states.append(neighbor_state)

    return neighbor_states


def find_path(neighbors_fn, game, goal_test):

    if goal_test(game):
        return (game["state"],)

    new_game = {
        "params": game["params"],
        "state": {
            "player position": game["state"]["player position"],
            "computer": game["state"]["computer"],
        },
    }

    initial_state = new_game["state"]

    initial_hashable_state = (
        game["state"]["player position"],
        frozenset(game["state"]["computer"]),
    )

    agenda = [(initial_state,)]

    visited = {initial_hashable_state}

    while agenda:
        this_path = agenda.pop(0)
        terminal_state = this_path[-1]

        new_game["state"] = terminal_state

        neighbor_states = neighbors_fn(new_game)
        for neighbor_state in neighbor_states:
            new_game["state"] = neighbor_state
            hashable_neighbor_state = (
                neighbor_state["player position"],
                frozenset(neighbor_state["computer"]),
            )

            if hashable_neighbor_state not in visited:
                new_path = this_path + (neighbor_state,)

                if goal_test(new_game):
                    return new_path

                agenda.append(new_path)
                visited.add(hashable_neighbor_state)

    return None


def compute_moves_from_path(path):
    positions = [state["player position"] for state in path]
    moves = []

    for (r1, c1), (r2, c2) in zip(positions, positions[1:]):
        if r2 == r1:
            moves.append("right" if c2 > c1 else "left")
        elif c2 == c1:
            moves.append("down" if r2 > r1 else "up")
    return moves


import json

if __name__ == "__main__":
    # level_description = [
    #     [["wall"], ["wall"], ["wall"], ["wall"], [], []],
    #     [["wall"], [], ["target"], ["wall"], [], []],
    #     [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
    #     [["wall"], ["target", "computer"], ["player"], [], [], ["wall"]],
    #     [["wall"], [], [], ["computer"], [], ["wall"]],
    #     [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
    #     [["wall"], ["wall"], ["wall"], ["wall"], [], []],
    # ]

    # game = make_new_game(level_description)
    # with open(
    #     os.path.join(TEST_DIRECTORY, "test_inputs/unit_movement_no_obstructions.txt")
    # ) as f:
    #     inputs = f.read().strip().splitlines(False)

    # for action in inputs:
    #     result = step_game(game, action)

    with open("puzzles/tiny_002.json") as f:
        level = json.load(f)

    game = make_new_game(level)

    result = solve_puzzle(game)
