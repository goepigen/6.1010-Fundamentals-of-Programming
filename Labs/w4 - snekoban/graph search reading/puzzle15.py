from pprint import pformat


def find_path(neighbors_fn, start, goal_test):
    if goal_test(start):
        return (start,)

    agenda = [(start,)]
    visited = {start}

    while agenda:
        this_path = agenda.pop(0)
        terminal_state = this_path[-1]

        for neighbor in neighbors_fn(terminal_state):
            if neighbor not in visited:
                breakpoint()
                new_path = this_path + (neighbor,)

                if goal_test(neighbor):
                    return new_path

                agenda.append(new_path)
                visited.add(neighbor)
    return None


def get_moveable_neighbors(row, col):
    return tuple(((row + i, col) for i in [1, -1] if row + i in range(4))) + tuple(
        ((row, col + i) for i in [1, -1] if col + i in range(4))
    )


def get_empty_square(state):
    return next(
        (
            (i, j)
            for i, row in enumerate(state)
            for j, val in enumerate(row)
            if val is None
        )
    )


def get_neighbor_states(state):
    empty_square_pos = get_empty_square(state)
    moveable_neighbor_pos = get_moveable_neighbors(*empty_square_pos)

    neighbor_states = []

    for row, col in moveable_neighbor_pos:
        new_state = [list(inner) for inner in state]
        neighbor = new_state[row][col]
        new_state[row][col] = None
        new_state[empty_square_pos[0]][empty_square_pos[1]] = neighbor
        neighbor_states.append(new_state)

    return tuple(
        tuple(tuple(row) for row in neighbor_state)
        for neighbor_state in neighbor_states
    )


if __name__ == "__main__":
    # test_graph = {
    #     13: [0, 77, 43],
    #     77: [-32, 28],
    #     43: [],
    #     0: [108],
    #     -32: [215, 42],
    #     28: [42],
    #     215: [42],
    #     42: [215],
    # }

    # def neighbors_fn(state):
    #     return test_graph.get(state, [])

    # result = find_path(neighbors_fn, 13, lambda state: state == -32)
    # initial_state = ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, 12, None), (13, 14, 10, 7))
    # goal_state = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, None))

    initial_state = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, None), (13, 14, 15, 12))

    goal_state = ((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, None))

    def goal_fn(state):
        return state == goal_state

    result = find_path(get_neighbor_states, initial_state, goal_fn)
