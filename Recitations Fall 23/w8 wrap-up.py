# 6.101 recitation: lab 8 wrapup

############################################ SAT

# helpers!

def variable(literal): # returns variable name
    pass
def literal_value(literal): # returns True or False
    pass

def is_trivially_true(formula): # returns boolean
    pass
def is_trivially_false(formula): # returns boolean
    pass

def substitute_in_clause(clause, var, value): # returns clause or True
    pass
def substitute_in_formula(formula, var, value): # returns formula
    pass

def pick_unit(formula): # returns literal of unit clause or None
    pass








############################################ Sudoku

# enabling print debugging as early as possible
def sudoku_board_to_sat_formula(sudoku_board):
    pass
def assignments_to_sudoku_board(assignments, n):
    pass
def board_to_string(board):
    pass




# representation for variables
#   the cell at row r and column c contains the value v

# string?
"row0col2is8"

# integer?
53

# something else?



# rules as helpers that generate parts of formula
def must_match_board(sudoku_board): # returns formula
    pass

def every_cell_has_some_valid_number(n):
    pass
def every_cell_has_at_most_one_number(n):
    pass


def sudoku_board_to_sat_formula(sudoku_board):
    n = len(sudoku_board)
    formula = []
    formula += must_match_board(sudoku_board)
    formula += every_cell_has_some_valid_number(n)
    formula += every_cell_has_at_most_one_number(n)
    ...
    return formula








def every_number_appears_in_row(r, n): # 0 <= r < n
    pass
def every_number_appears_in_column(c, n): # 0 <= c < n
    pass
def every_number_appears_in_block(b, n): # 0 <= b < n, blocks are numbered left-right, then top-down
    pass








def every_number_appears_in_group(group, n):
    """
    group is an iterable of (r,c) cell coordinates, 0 <= r,c < n
    """
    return [
        [ ((r,c,v),True) for (r,c) in group ]
            for v in range(1,n+1)
    ]

def cells_in_row(r, n):
    """returns a list of the coordinates of all cells in row r"""
    pass
def cells_in_column(c, n):
    """yields the coordinates of all cells in column c"""
    pass
def cells_in_block(b, n):
    """yields the coordinates of all cells in block b (numbered left-to-right, top-to-bottom)"""
    pass





