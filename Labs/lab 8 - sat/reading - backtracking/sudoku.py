import time


def format_sudoku(board):
    if not board:
        return "Failed"
    _divider = "+" + "".join("-+" if i % 3 == 2 else "-" for i in range(9))
    lines = []
    for i in range(9):
        if i % 3 == 0:
            lines.append(_divider)
        line = "|"
        for j in range(9):
            line += " " if board[i][j] == 0 else str(board[i][j])
            if j % 3 == 2:
                line += "|"
        lines.append(line)
    lines.append(_divider)
    return "\n".join(lines)


# INITIAL VERSION


def solve_sudoku(board):

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                continue

            # Found a 0; try filling it with each of the numbers 1-9
            for trial in range(1, 10):
                # create a new board with the 0 filled with a number
                new_board = [
                    [trial if (r, c) == (row, col) else board[r][c] for c in range(9)]
                    for r in range(9)
                ]
                # check if the new board satisfies the rules of a sudoku board
                if valid_board(new_board):
                    # if it does, try solving the new board
                    result = solve_sudoku(new_board)
                    # if we were able to solve the new board, then return it
                    if result is not None:
                        return result
            # we tried to fill the first non-empty position with a number
            # and no solution was found for any of the trials.
            # Thus, no solution is possible.
            return None
    # if there are no empty squares, then return the board.
    return board


def violation(l):
    return sum(set(l)) != sum(l)


def valid_board(board):
    rows = board
    cols = list(zip(*rows))
    subgrids = [
        [board[3 * i + k1][3 * j + k2] for k1 in range(3) for k2 in range(3)]
        for i in range(3)
        for j in range(3)
    ]

    blocks = rows + cols + subgrids

    for block in blocks:
        if violation(block):
            return False
    return True


# IMPROVED VERSION


def solve_sudoku2(board):

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                continue

            # Found a 0; try filling it with each of the possible
            # remaining numbers for that position
            for trial in valid_moves(board, row, col):
                # create a new board with the 0 filled with a number
                new_board = [
                    [trial if (r, c) == (row, col) else board[r][c] for c in range(9)]
                    for r in range(9)
                ]

                result = solve_sudoku2(new_board)
                # if we were able to solve the new board, then return it
                if result is not None:
                    return result
            # we tried to fill the first non-empty position with a number
            # and no solution was found for any of the trials.
            # Thus, no solution is possible.
            return None
    # if there are no empty squares, then return the board.
    return board


def valid_moves(board, row, col):
    return (
        set(range(1, 10))
        - values_in_row(board, row)
        - values_in_col(board, col)
        - values_in_subgrid(board, row, col)
    )


def values_in_row(board, r):
    return {el for el in board[r] if el != 0}


def values_in_col(board, c):
    col_vals = [board[r][c] for r in range(len(board))]
    return {el for el in col_vals if el != 0}


def values_in_subgrid(board, r, c):
    sr = r // 3
    sc = c // 3
    subgrid = [board[3 * sr + k1][3 * sc + k2] for k1 in range(3) for k2 in range(3)]
    return {el for el in subgrid if el != 0}


# VERSION WITH MUTATION


def solve_sudoku_mut(board):

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                continue

            # Found a 0; try filling it with each of the possible
            # remaining numbers for that position
            for trial in valid_moves(board, row, col):
                # create a new board with the 0 filled with a number
                board[row][col] = trial

                result = solve_sudoku_mut(board)
                # if we were able to solve the new board, then return it
                if result is not None:
                    return result
            # we tried to fill the first non-empty position with a number
            # and no solution was found for any of the trials.
            # Thus, no solution is possible.
            board[row][col] = 0
            return None
    # if there are no empty squares, then return the board.
    return board


if __name__ == "__main__":
    grid1 = [
        [5, 1, 7, 6, 0, 0, 0, 3, 4],
        [2, 8, 9, 0, 0, 4, 0, 0, 0],
        [3, 4, 6, 2, 0, 5, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 0, 1, 0],
        [0, 3, 8, 0, 0, 6, 0, 4, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 7, 8],
        [7, 0, 3, 4, 0, 0, 5, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    t = time.time()
    res = solve_sudoku_mut(grid1)
    elapsed = time.time() - t
    if res:
        print(format_sudoku(res))
        print(f"completed in {elapsed} seconds")
    else:
        print("Failed")

# TESTS


def test_valid_moves():
    board = [
        [5, 1, 7, 6, 0, 0, 0, 3, 4],
        [2, 8, 9, 0, 0, 4, 0, 0, 0],
        [3, 4, 6, 2, 0, 5, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 0, 1, 0],
        [0, 3, 8, 0, 0, 6, 0, 4, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 7, 8],
        [7, 0, 3, 4, 0, 0, 5, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    vm = valid_moves(board, 0, 3)
    assert vm == {8, 9}, "Incorrect valid moves"


def test_values_in_subgrid():
    board = [
        [5, 1, 7, 6, 0, 0, 0, 3, 4],
        [2, 8, 9, 0, 0, 4, 0, 0, 0],
        [3, 4, 6, 2, 0, 5, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 0, 1, 0],
        [0, 3, 8, 0, 0, 6, 0, 4, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 7, 8],
        [7, 0, 3, 4, 0, 0, 5, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    subgrid = values_in_subgrid(board, 0, 3)

    assert subgrid == {6, 4, 2, 5}, "Incorrect subgrid."


def test_values_in_col():
    board = [
        [5, 1, 7, 6, 0, 0, 0, 3, 4],
        [2, 8, 9, 0, 0, 4, 0, 0, 0],
        [3, 4, 6, 2, 0, 5, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 0, 1, 0],
        [0, 3, 8, 0, 0, 6, 0, 4, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 7, 8],
        [7, 0, 3, 4, 0, 0, 5, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    col_values = values_in_col(board, 5)

    assert col_values == {4, 5, 6}


def test_valid_board():
    # empty board
    board = [[0] * 9 for _ in range(9)]
    assert valid_board(board), "An empty board is valid, but got invalid."

    # same value in a row
    board = [[0] * 9 for _ in range(9)]
    board[0][1] = 1
    board[0][6] = 1
    assert not valid_board(board), "Same value in same row invalidates the board."

    # same value in a column
    board = [[0] * 9 for _ in range(9)]
    board[5][1] = 4
    board[7][1] = 4
    assert not valid_board(board), "Same value in same column invalidates the board."

    # same value in a subgrid
    board = [[0] * 9 for _ in range(9)]
    board[0][0] = 1
    board[2][2] = 1
    assert not valid_board(board), "Same value in same subgrid invalidates the board."
