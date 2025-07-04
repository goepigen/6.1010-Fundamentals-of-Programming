from find_path import find_path  # this is the last find_path() from the reading
import time

##### FREE FOOD BONANZA!


def free_food_bonanza(initial_board):
    """
    You belong to a student group that is investing in writing a Python program
    to plot out the shortest path through space to collect all the free food
    that is available at some moment in time.  Write a function that takes in a
    two-dimensional grid with positions of free food and a hungry student.  The
    function should return the minimum number of steps needed for the student to
    enter all of the squares with food.  The student can move up, down, left, or
    right on any given step.  If the student has no way to collect all the food,
    return None.

    The grid comes in as a nested list, where each cell holds one of:
    - 'S' for student (exactly one on the board)
    - 'F' for food (arbitrarily many on the board)
    - 'W' for wall (arbitrarily many on the board, student may not walk through
    them)
    - ' ' for an empty square

    """

    def make_state_from_board(board):
        pass

    def neighbors(state):
        pass

    def goal(state):
        pass

    start = make_state_from_board(initial_board)
    path = find_path(neighbors, start, goal)
    return None  # TODO: what to return here?


def test_small():
    board1 = [["S", " ", " ", " ", "F"]]

    board2 = [
        ["F", " ", " ", " ", " "],
        ["W", "W", "S", "W", "F"],
        [" ", " ", " ", "W", " "],
    ]

    board3 = [
        ["W", " ", " ", "W", "F"],
        ["W", "W", " ", " ", "F"],
        ["W", " ", " ", " ", " "],
        [" ", "S", "F", " ", " "],
        ["F", "F", "F", " ", " "],
    ]

    expected_results = [4, 8, 10]

    for b, r in zip([board1, board2, board3], expected_results):
        assert free_food_bonanza(b) == r


def test_large():
    board_sizes = [10, 20, 40, 80]
    for N in board_sizes:
        board = [[" " for _ in range(N)] for _ in range(N)]
        board[0][0] = "S"
        board[N - 1][N - 1] = "F"
        board[N // 2][N // 2] = "F"
        board[0][N - 1] = "F"
        board[N - 1][0] = "F"
        print(f"Testing Board Size: {N}")
        start = time.time()
        out = free_food_bonanza(board)
        print(f"Run Took: {time.time() - start}")
        assert out == 4 * N - 5


if __name__ == "__main__":
    test_small()
    test_large()
