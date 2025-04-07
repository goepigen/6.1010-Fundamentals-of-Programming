"""
6.101 Lab:
Bacon Number
"""

#!/usr/bin/env python3

import pickle

# import typing # optional import
# import pprint # optional import

# NO ADDITIONAL IMPORTS ALLOWED!

KEVIN_BACON_ID = 4724


def transform_data(raw_data):
    """
    Given raw_data, transform into a dictionary where keys are all the actor_id's that appear
    in the list, and values are sets of actors the actor_id has acted with (ids of actors that
    have appeared in some tuple with actor_id).

    Args:
        raw_data: list of (actor_id_1, actor_id_2, film_id)
    Returns:
        dictionary: dictionary { actor_id: { actor_id's } }
    """
    tdb = {}

    def add_tdb_entry(actor_id_1, actor_id_2):
        if actor_id_1 in tdb:
            tdb[actor_id_1].add(actor_id_2)
        else:
            tdb[actor_id_1] = {actor_id_2}

    for actor_id1, actor_id2, _ in raw_data:
        add_tdb_entry(actor_id1, actor_id2)
        add_tdb_entry(actor_id2, actor_id1)

    return tdb


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Given a dictionary of actor_id/set of actor ids pairs, checks whether value actor_id_2
    is contained in the set of values associated with key actor_id_1 in the dictionary.

    Args:
        transformed data: dictionary { actor_id: { actor_id's } }
    Returns"
        boolean
    """
    if actor_id_1 == actor_id_2:
        return True
    return actor_id_2 in transformed_data.get(actor_id_1, set())


def actors_with_bacon_number(transformed_data, bacon_number):
    """
    Given a dictionary of actor_id/set of actor id pairs, obtains the set of values (actor ids)
    associated with Kevin Bacon's id in the dictionary (bacon number 1), then obtains the
    values in the dictionary associated with those ids (bacon number 2), and so on until the set obtained
    is associated with bacon number bacon_number, at which point the set of ids is returned.

    Args:
        transformed data: dictionary { actor_id: { actor_id's } }
        bacon_number: int
    Returns:
        Set of actor_id's with bacon number bacon_number

    """
    current_bn = 0
    visited = {KEVIN_BACON_ID}
    current = {KEVIN_BACON_ID}
    actors_with_prev_bn = {KEVIN_BACON_ID}

    while current_bn < bacon_number and actors_with_prev_bn:
        current = set()
        for prev_id in actors_with_prev_bn:
            for id in transformed_data[prev_id]:
                if id not in visited:
                    current.add(id)
                    visited.add(id)
        current_bn += 1
        actors_with_prev_bn = current
    return current


def bacon_path(transformed_data, actor_id):
    return actor_to_actor_path(transformed_data, KEVIN_BACON_ID, actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    if actor_id_1 == actor_id_2:
        return (actor_id_1,)

    visited = {actor_id_1}

    # paths starting at actor_id
    paths = {0: [(actor_id_1,)]}

    # the length of shortest paths currently in paths variable
    cur_len = 0

    found = False

    while paths and not found:
        # get the last path in the list of paths with current shortest length
        path = paths[cur_len].pop()
        print(path)

        # get the last actor_id in path
        last_id_in_path = path[-1]

        # get potential next actors to add to path
        next_ids = transformed_data[last_id_in_path]
        for id in next_ids:
            if id not in visited:
                # create a new path with one extra actor id
                new_path = (*path, id)
                paths.setdefault(cur_len + 1, []).append(new_path)
                visited.add(id)
                if id == actor_id_2:
                    # if we reach actor_id_2, we break out of the for loop.
                    found = True
                    return new_path
        # if we popped the last path with length cur_len then remove that key and increment cur_len
        # so we can check paths with one extra element
        if not paths[cur_len]:
            del paths[cur_len]
            cur_len += 1

    return None


def actor_path(transformed_data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == "__main__":
    with open("resources/tiny.pickle", "rb") as f:
        tiny_db = pickle.load(f)

    with open("resources/small.pickle", "rb") as f:
        small_db = pickle.load(f)

    with open("resources/large.pickle", "rb") as f:
        large_db = pickle.load(f)

    with open("resources/names.pickle", "rb") as f:
        names = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.

    large_tdb = transform_data(large_db)
    small_tdb = transform_data(small_db)
    tiny_tdb = transform_data(tiny_db)

    # sum([len(actors_with_bacon_number(tdb, i)) for i in range()])

    actor_id = 197897

    first_result = bacon_path(large_tdb, actor_id)

    # second_result = lab.bacon_path(small_tdb, actor_id)
