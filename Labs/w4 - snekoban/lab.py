"""
6.1010 Lab:
Snekoban Game
"""

# import json # optional import for loading test_levels
# import typing # optional import
# import pprint # optional import

# NO ADDITIONAL IMPORTS!
import os
import time

TEST_DIRECTORY = os.path.dirname(__file__)

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
        "player position": None,
        "wall": set(),
        "computer": set(),
        "target": set(),
        "empty": set(),
        "width": width,
        "height": height,
    }

    for row_i, _ in enumerate(level_description):
        for col_j, __ in enumerate(level_description[row_i]):
            position = (row_i, col_j)
            objs = level_description[row_i][col_j]
            if not objs:
                game["empty"].add(position)
            else:
                for obj in objs:
                    if obj == "wall":
                        game["wall"].add(position)
                    elif obj == "target":
                        game["target"].add(position)
                    elif obj == "computer":
                        game["computer"].add(position)
                    elif obj == "player":
                        game["player position"] = position
    return {
        **game,
        "wall": frozenset(game["wall"]),
        "target": frozenset(game["target"]),
    }


def victory_check(game):
    """
    Given a game representation (of the form returned from make_new_game),
    return a Boolean: True if the given game satisfies the victory condition,
    and False otherwise.
    """
    if not game["target"] or not game["computer"]:
        return False

    return game["target"] == game["computer"]


def step_game(game, direction):
    """
    Given a game representation (of the form returned from make_new_game),
    return a game representation (of that same form), representing the
    updated game after running one step of the game.  The user's input is given
    by direction, which is one of the following:
        {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    new_game = {
        **game,
        "player position": game["player position"],
        "computer": set(game["computer"]),
        "empty": set(game["empty"]),
    }

    player_pos = new_game["player position"]
    adjacent_pos = tuple(
        (v1 + v2 for v1, v2 in zip(player_pos, DIRECTION_VECTOR[direction]))
    )

    # If adjacent position is a wall, do nothing and return.
    if adjacent_pos in new_game["wall"]:
        return new_game

    # Get the objects in the adjacent position
    adjacent_objs = get_objects_at_position(new_game, adjacent_pos)
    # If adjacent position is a computer
    if "computer" in adjacent_objs:
        # get the adjacent to the computer position
        computer_adjacent_pos = tuple(
            (v1 + v2 for v1, v2 in zip(adjacent_pos, DIRECTION_VECTOR[direction]))
        )
        # if the adjacent position to the computer contains a wall or another computer, do
        # nothing and return.
        if (
            computer_adjacent_pos in new_game["wall"]
            or computer_adjacent_pos in new_game["computer"]
        ):
            return new_game
        # if the adjacent position to the computer position is empty or contains a target (and
        # since we've already checked for a computer in this position we know the target is by
        # itself) then move the player, move the computer, and return.
        if (
            computer_adjacent_pos in new_game["empty"]
            or computer_adjacent_pos in new_game["target"]
        ):
            update_player_position(new_game, player_pos, adjacent_pos)
            # move the computer
            new_game["computer"].remove(adjacent_pos)
            new_game["computer"].add(computer_adjacent_pos)
            # if the new computer position was originally empty, remove that position from the
            # empty positions in game
            if computer_adjacent_pos in new_game["empty"]:
                new_game["empty"].remove(computer_adjacent_pos)
            return new_game
    # If adjacent position is a target (note that we know at this point that there is no computer
    # in this position), move the player to the adjacent position.
    elif "target" in adjacent_objs or "empty" in adjacent_objs:
        update_player_position(new_game, player_pos, adjacent_pos)
        return new_game


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

    width = game["width"]
    height = game["height"]

    level_representation = [[[] for i in range(width)] for j in range(height)]

    for k, v in game.items():
        if k in ["width", "height", "empty"]:
            continue
        if k == "player position":
            level_representation[v[0]][v[1]].append("player")
        else:
            for pos in v:
                level_representation[pos[0]][pos[1]].append(k)

    return level_representation


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from make_new_game), find
    a solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    game_params = {
        "wall": game["wall"],
        "target": game["target"],
        "width": game["width"],
        "height": game["height"],
    }

    initial_state = get_state_with_last_direction(game)

    state_path_with_directions = find_path(
        get_neighbor_states, initial_state, game_params, victory_check
    )

    if state_path_with_directions is None:
        return None

    return [state[0] for state in state_path_with_directions[1:]]


# HELPERS
def get_state_with_last_direction(game, last_direction=None):
    return (
        last_direction,
        game["player position"],
        frozenset(game["computer"]),
        frozenset(game["empty"]),
    )


def get_full_state(state, game_params):
    return {
        **game_params,
        "player position": state[1],
        "computer": set(state[2]),
        "empty": set(state[3]),
    }


def get_neighbor_states(game):
    neighbor_states = []
    neighbor_full_states = []
    t0 = time.time()
    for direction in DIRECTION_VECTOR:
        t = time.time()
        neighbor_full_state = step_game(game, direction)
        t1 = time.time()
        neighbor_state = get_state_with_last_direction(neighbor_full_state, direction)
        t2 = time.time()
        neighbor_states.append(neighbor_state)
        t3 = time.time()
        neighbor_full_states.append(neighbor_full_state)
        t4 = time.time()
    print(
        f"Total time: {time.time()-t0:.6f}, 1: {t1-t:.6f}, 2: {t2-t1:.6f}, 3: {t3-t2:.6f}, 4: {t4-t3:.6f}"
    )
    return [neighbor_states, neighbor_full_states]


def find_path(neighbors_fn, initial_state, game_params, goal_test):
    game = get_full_state(initial_state, game_params)

    if goal_test(game):
        return (initial_state,)

    agenda = [(initial_state,)]
    visited = {initial_state}

    sum = 0
    tt = time.time()
    while agenda:
        this_path = agenda.pop(0)
        terminal_state = this_path[-1]
        game = get_full_state(terminal_state, game_params)

        t0 = time.time()
        neighbors = neighbors_fn(game)
        t1 = time.time()
        sum += t1 - t0
        for neighbor_state, game in zip(*neighbors):
            # start_time = time.time()
            if neighbor_state not in visited:
                new_path = this_path + (neighbor_state,)

                if goal_test(game):
                    print(sum, f"{time.time() - tt: .6f}")
                    return new_path

                agenda.append(new_path)
                visited.add(neighbor_state)
            # t1 = time.time()

            # print(f"{t1 - start_time:.6f}")
    return None


def update_player_position(game, player_pos, adjacent_pos):
    # check objects in the player's original position
    objs_at_player_position = get_objects_at_position(game, player_pos)
    # if there are no objects (ie, if there was no target in that position)
    if not objs_at_player_position:
        # then the original player position becomes empty
        game["empty"].add(player_pos)
    # move the player to the adjacent position
    game["player position"] = adjacent_pos
    # if the adjacent position was empty, remove that position from the empty positions
    if adjacent_pos in game["empty"]:
        game["empty"].remove(adjacent_pos)


def get_objects_at_position(game, position):
    objects = set()
    if position in game["empty"]:
        objects.add("empty")
    if position in game["target"]:
        objects.add("target")
    if position in game["computer"]:
        objects.add("computer")
    if position in game["wall"]:
        objects.add("wall")

    return objects


if __name__ == "__main__":
    level_description = [
        [["wall"], ["wall"], ["wall"], ["wall"], [], []],
        [["wall"], [], ["target"], ["wall"], [], []],
        [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
        [["wall"], ["target", "computer"], ["player"], [], [], ["wall"]],
        [["wall"], [], [], ["computer"], [], ["wall"]],
        [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
        [["wall"], ["wall"], ["wall"], ["wall"], [], []],
    ]

    game = make_new_game(level_description)
    # with open(
    #     os.path.join(TEST_DIRECTORY, "test_inputs/unit_movement_no_obstructions.txt")
    # ) as f:
    #     inputs = f.read().strip().splitlines(False)

    # for action in inputs:
    #     result = step_game(game, action)

    result = solve_puzzle(game)
