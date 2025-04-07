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

    def add_tdb_entry(actor_id_1, actor_id_2, film_id):
        tdb.setdefault(actor_id_1, {}).setdefault(actor_id_2, set()).add(film_id)

    for actor_id_1, actor_id_2, film_id in raw_data:
        add_tdb_entry(actor_id_1, actor_id_2, film_id)
        add_tdb_entry(actor_id_2, actor_id_1, film_id)

    return tdb


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Given a dictionary of actor_id/set of actor ids pairs, checks whether value actor_id_2
    is contained in the set of values associated with key actor_id_1 in the dictionary.

    Args:
        transformed data: dictionary { actor_id: { actor_id's } }
        actor_id_1: int
        actor_id_2: int
    Returns"
        bool: True if actor_id_1 and actor_id_2 have acted together
    """
    if actor_id_1 == actor_id_2:
        return True

    return actor_id_2 in transformed_data.get(actor_id_1, {})


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
            for id in list(transformed_data[prev_id]):
                if id not in visited:
                    current.add(id)
                    visited.add(id)
        current_bn += 1
        actors_with_prev_bn = current
    return current


def bacon_path(transformed_data, actor_id):
    """
    Given a dictionary of actor_id/set of actor id pairs, obtains a tuple of actor_ids starting with
    the id of Kevin Bacon and ending with actor_id.
    Args:
        transformed data: dictionary { actor_id: { actor_id's } }
        actor_id: int
    Returns:
        If a path is found, returns a tuple of actor ids, starting with Kevin Bacon's id, ending with actor_id.
        If a path is not found, returns None.
    """
    return actor_to_actor_path(transformed_data, KEVIN_BACON_ID, actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Given a dictionary of actor_id/set of actor id pairs and two actor_ids, obtains a tuple of
    actor_ids starting with actor_id_1 and ending with actor_id_2, representing a path in which each
    successive actor has acted with the actors just before and just after in the path.
    The path represents a way to go from actor_id_1 to actor_id_2 through such "acted together"
    relationships. If no path is found, None is returned.

    Args:
        transformed data: dictionary { actor_id: { actor_id's } }
        actor_id_1: int
        actor_id_2: int
    Returns:
        If a path is found, returns a tuple of actor ids, starting with actor_id_1, ending with actor_id_2.
        If a path is not found, returns None.
    """
    path = actor_to_actor_path_with_films(transformed_data, actor_id_1, actor_id_2)

    return tuple(item[1] for item in path) if path is not None else None


def actor_to_actor_path_with_films(transformed_data, actor_id_1, actor_id_2):
    goal_test_fn = lambda actor_id: actor_id == actor_id_2
    return actor_to_goal_path_with_films(transformed_data, actor_id_1, goal_test_fn)


def actor_to_goal_path_with_films(transformed_data, actor_id_1, goal_test_fn):
    """
    Given a dictionary of actor_id/set of actor id pairs and two actor_ids, obtains a tuple of
    actor_ids starting with actor_id_1 and ending with actor_id_2, representing a path in which each
    successive actor has acted with the actors just before and just after in the path.
    The path represents a way to go from actor_id_1 to actor_id_2 through such "acted together"
    relationships. If no path is found, None is returned.

    Args:
        transformed data: dictionary { actor_id: { actor_id's } }
        actor_id_1: int
        actor_id_2: int
    Returns:
        If a path is found, returns a tuple of actor ids, starting with actor_id_1, ending with actor_id_2.
        If a path is not found, returns None.
    """
    if goal_test_fn(actor_id_1):
        return ((None, actor_id_1, None),)

    paths = [((None, actor_id_1, None),)]

    visited = {actor_id_1}

    while paths:
        new_paths = []

        for path in paths:
            last_id_in_path = path[-1][1]

            # get potential next actors to add to path
            acted_with = transformed_data[last_id_in_path]

            for actor_id, film_ids in acted_with.items():
                if actor_id in visited:
                    continue

                new_path = (*path, (last_id_in_path, actor_id, film_ids))
                if goal_test_fn(actor_id):
                    return new_path

                new_paths.append(new_path)
                visited.add(actor_id)

        paths = new_paths

    return None


with open("resources/movies.pickle", "rb") as f:
    movies_db = pickle.load(f)

movie_id_to_name = {v: k for k, v in movies_db.items()}

with open("resources/names.pickle", "rb") as f:
    names = pickle.load(f)


def actor_to_actor_film_path(transformed_data, actor_1, actor_2):
    # Convert actor names to IDs if necessary
    if isinstance(actor_1, str):
        actor_1 = names[actor_1]
    if isinstance(actor_2, str):
        actor_2 = names[actor_2]

    path_with_films = actor_to_actor_path_with_films(transformed_data, actor_1, actor_2)

    return tuple(
        [movie_id_to_name[movie_id] for movie_id in item[2]]
        for item in path_with_films[1:]
    )


def actor_path(transformed_data, actor_id, goal_test_fn):
    path = actor_to_goal_path_with_films(transformed_data, actor_id, goal_test_fn)
    return [item[1] for item in path] if path is not None else None


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


# HELPERS


def verify_path(tdb, path):
    return (
        sum([path[i + 1] in tdb[actor_id] for i, actor_id in enumerate(path[0:-1])])
        == len(path) - 1
    )


if __name__ == "__main__":
    with open("resources/tiny.pickle", "rb") as f:
        tiny_db = pickle.load(f)

    with open("resources/small.pickle", "rb") as f:
        small_db = pickle.load(f)

    with open("resources/large.pickle", "rb") as f:
        large_db = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.

    large_tdb = transform_data(large_db)
    small_tdb = transform_data(small_db)
    tiny_tdb = transform_data(tiny_db)

    # sum([len(actors_with_bacon_number(tdb, i)) for i in range()])

    # actor_id = 197897

    # first_result = bacon_path(large_tdb, actor_id)

    # second_result = lab.bacon_path(small_tdb, actor_id)

    actor_1 = 1345462
    actor_2 = 89614
    len_expected = 7

    first_result = actor_to_actor_path(large_tdb, actor_1, actor_2)

    film_result = actor_to_actor_film_path(large_tdb, actor_1, actor_2)

    question = actor_to_actor_film_path(large_tdb, "Gregg Henry", "Anton Radacic")
