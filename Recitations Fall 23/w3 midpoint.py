# 6.101 recitation: lab 3 midpoint

############## Reachability: can you get there without going outside?

def can_reach(map, start_building, goal_building):
    """
    map: dictionary where each key is a building name (string), mapping to a set of its directly-connected neighbors
    start_building: building to start from
    goal_building: building you're trying to reach

    returns True if and only if you can get from start_building to goal_building through
        directly-connected neighbors, i.e. without going outside
    """



# from http://whereis.mit.edu/?zoom=18&lat=42.36162996081668&lng=-71.09057574701308&maptype=mit&open=-1
# (and not using tunnels)
small_map = {
    '26': {'36'}, # 26 connects to 36
    '32': {'36'}, # 32 connects to 36
    '36': {'26', '32'}, # 36 connects to both of the others
    '76': set()   # Koch building is by itself
}

def test_can_reach_small():
    assert can_reach(small_map, '26', '32')
    assert can_reach(small_map, '76', '76')
    assert not can_reach(small_map, '76', '32')






############## outline of solution (from reading)

# def can_reach(map, start_building, goal_building):
#     """
#     map: dictionary { `building` : set of the directly-connected neighbors of `building` }
#     start_building: building to start from
#     goal_building: building you're trying to reach

#     returns True if and only if you can get from start_building to goal_building through
#         directly-connected neighbors, i.e. without going outside
#     """

#     # helper function to get neighbors of building
#     def get_neighbors(building):
#         ________
    
#     agenda = [ ________ ]   # agenda: buildings still to explore
#     visited = { ________ }  # visited set: all buildings ever added to the agenda

#     # while there are still buildings to explore
#     while agenda:
#         # remove a building from the agenda
#         building = ________

#         # add each neighbor to agenda
#         for neighbor in get_neighbors(building):
#             ...

#     return _________









############## Path finding: what is the actual path?


def find_path(map, start_building, goal_building):
    """
    same arguments as can_reach()

    returns path of directly-connected buildings from start_building to goal_building,
    or None if no possible path in map
    """


# def test_find_path_small():
#     assert find_path(small_map, '26', '32') == ('26', '36', '32')
#     assert find_path(small_map, '76', '76') == ('76',)
#     assert find_path(small_map, '76', '32') == None

# def can_reach(map, start_building, goal_building):
#     _______









############## Does it work on bigger maps?
############## (and let's also include tunnels in adjacency)


# from http://whereis.mit.edu/?zoom=17&lat=42.35983737457077&lng=-71.09177737665175&maptype=mit&open=-1
large_map = {
 '1': {'5', '3'},
 '10': {'4', '3'},
 '11': {'3'},
 '12': {'16', '13', '26'},
 '13': {'9', '12'},
 '14': {'18', '2'},
 '16': {'56', '8', '12'},
 '17': {'33'},
 '18': {'56', '14'},
 '2': {'14', '6', '4'},
 '24': {'34'},
 '26': {'32', '12', '36'},
 '3': {'7', '11', '1', '10'},
 '31': {'37'},
 '32': {'26', '57', '36'},
 '33': {'9', '17', '35'},
 '34': {'36', '24', '38'},
 '35': {'37', '33'},
 '36': {'32', '26', '34'},
 '37': {'39', '31', '35'},
 '38': {'39', '34'},
 '39': {'37', '38'},
 '4': {'2', '8', '10'},
 '41': {'42'},
 '42': {'43', '41'},
 '43': {'42'},
 '45': {'46'},
 '46': {'45'},
 '48': set(),
 '5': {'7', '1'},
 '50': set(),
 '54': set(),
 '56': {'16', '66', '18'},
 '57': {'32'},
 '6': {'2', '8', '6C'},
 '62': {'64'},
 '64': {'62'},
 '66': {'56', '68', 'E17'},
 '68': {'66'},
 '6C': {'6', '8'},
 '7': {'5', '9', '3', '7A'},
 '76': set(),
 '7A': {'7'},
 '8': {'6', '4', '6C', '16'},
 '9': {'7', '13', '33'},
 'E1': set(),
 'E14': {'E15'},
 'E15': {'E14'},
 'E17': {'E18', '66'},
 'E18': {'E25', 'E19', 'E17'},
 'E19': {'E18'},
 'E2': set(),
 'E23': {'E25'},
 'E25': {'E18', 'E23'},
 'E28': set()
}

# print(f"{find_path(large_map, '1', '2')=}")
# print(f"{find_path(large_map, '1', '32')=}")
# print(f"{find_path(large_map, '7', '62')=}")
