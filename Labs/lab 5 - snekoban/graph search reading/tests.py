import puzzle15
from pprint import pformat
import difflib


def test_get_moveable_neighbors_top_left():
    # Top-left corner of the board
    row = 0
    col = 0
    result = puzzle15.get_moveable_neighbors(row, col)
    expected = ((1, 0), (0, 1))

    assert result == expected, f"Wrong neighbors for position ({row}, {col})."


def test_get_moveable_neighbors_right_border():
    # Right border of the board, not on a corner. Three neighbors.
    row = 1
    col = 3
    result = puzzle15.get_moveable_neighbors(row, col)
    expected = ((2, 3), (0, 3), (1, 2))

    assert result == expected, f"Wrong neighbors for position ({row}, {col})."


def test_get_moveable_neighbors_middle_of_board():
    # A position with four neighbors.
    row = 1
    col = 2
    result = puzzle15.get_moveable_neighbors(row, col)
    expected = ((2, 2), (0, 2), (1, 3), (1, 1))

    assert result == expected, f"Wrong neighbors for position ({row}, {col})."


def test_empty_square():
    state = ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, 12, None), (13, 14, 10, 7))
    empty_square_pos = puzzle15.get_empty_square(state)
    expected = (2, 3)

    assert (
        empty_square_pos == expected
    ), f"Expected empty square at {expected} but got {empty_square_pos}."


def test_get_neighbor_states():
    state = ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, 12, None), (13, 14, 10, 7))
    neighbor_states = puzzle15.get_neighbor_states(state)

    expected_neighbor_states = (
        ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, 12, 7), (13, 14, 10, None)),
        ((2, 6, 3, 15), (11, 9, 4, None), (1, 8, 12, 5), (13, 14, 10, 7)),
        ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, None, 12), (13, 14, 10, 7)),
    )

    assert neighbor_states == expected_neighbor_states, (
        "Neighbor states not as expected\n\n"
        f"Expected:\n{pformat(expected_neighbor_states)}\n\n"
        f"Got:\n{pformat(neighbor_states)}"
    )


def test_get_neighbor_states_diff():
    state = ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, 12, None), (13, 14, 10, 7))
    neighbor_states = puzzle15.get_neighbor_states(state)

    expected_neighbor_states = (
        ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, 12, 7), (13, 14, 10, None)),
        ((2, 6, 3, 15), (11, 9, 4, None), (1, 8, 12, 5), (13, 14, 10, 7)),
        ((2, 6, 3, 15), (11, 9, 4, 5), (1, 8, None, 12), (13, 14, 10, 7)),
    )

    expected_str = pformat(expected_neighbor_states)
    actual_str = pformat(neighbor_states)

    diff = "\n".join(
        difflib.unified_diff(
            expected_str.splitlines(),
            actual_str.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm="",
        )
    )

    assert neighbor_states == expected_neighbor_states, f"Mismatch:\n{diff}"
