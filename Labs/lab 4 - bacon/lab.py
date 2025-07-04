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
    Transforms raw_data into a dictionary.

    Args:
        raw_data: list of (actor_id_1, actor_id_2, film_id)
    Returns:
        dictionary:
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
    """
    tdb = {"actors": {}, "films": {}}

    def add_tdb_actor_entry(actor_id_1, actor_id_2, film_id):
        tdb["actors"].setdefault(actor_id_1, {}).setdefault(actor_id_2, set()).add(
            film_id
        )

    def add_tdb_film_entry(actor_id_1, actor_id_2, film_id):
        tdb["films"].setdefault(film_id, set()).update([actor_id_1, actor_id_2])

    for actor_id_1, actor_id_2, film_id in raw_data:
        add_tdb_actor_entry(actor_id_1, actor_id_2, film_id)
        add_tdb_actor_entry(actor_id_2, actor_id_1, film_id)
        add_tdb_film_entry(actor_id_1, actor_id_2, film_id)

    return tdb


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Returns True if actors 1 and 2 have acted together in a movie, False otherwise.

    Args:
        transformed data:
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
        actor_id_1: int
        actor_id_2: int
    Returns"
        bool: True if actor_id_1 and actor_id_2 have acted together
    """
    if actor_id_1 == actor_id_2:
        return True

    return actor_id_2 in transformed_data["actors"].get(actor_id_1, {})


def actors_with_bacon_number(transformed_data, bacon_number):
    """
    Returns a set of the actor_id's that have bacon number bacon_number.

    Args:
        transformed data:
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
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
            for id in list(transformed_data["actors"][prev_id]):
                if id not in visited:
                    current.add(id)
                    visited.add(id)
        current_bn += 1
        actors_with_prev_bn = current
    return current


def bacon_path(transformed_data, actor_id):
    """
    Returns a tuple of actor_ids starting with the id of Kevin Bacon and ending with actor_id.
    This tuple represents a chain of "acted together" relationships between any two adjacent actors
    in the list.
    Args:
        transformed data
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
        actor_id: int
    Returns:
        If a path is found, returns a tuple of actor ids, starting with Kevin Bacon's id, ending with actor_id.
        If a path is not found, returns None.
    """
    return actor_to_actor_path(transformed_data, KEVIN_BACON_ID, actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Returns a tuple of shortest length of actor_ids starting with actor_id_1 and ending with actor_id_2,
    representing a path in which each successive actor has acted with the adjacent actors the tuple.
    The path represents a way to go from actor_id_1 to actor_id_2 through such "acted together"
    relationships. If no path is found, None is returned.

    Args:
        transformed data:
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
        actor_id_1: int
        actor_id_2: int
    Returns:
        If a path is found, returns a tuple of actor ids, starting with actor_id_1, ending with actor_id_2.
        If a path is not found, returns None.
    """
    path = actor_to_actor_path_with_films(transformed_data, actor_id_1, actor_id_2)

    return tuple(item[1] for item in path) if path is not None else None


def actor_to_actor_path_with_films(transformed_data, actor_id_1, actor_id_2):
    """
    Returns a path from actor_id_1 to actor_id_2 that includes, for each "acted with" relationship in the path
    (a tuple), the film the actors acted together in.

    Args:
        transformed_data:
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
        actor_id_1: int
        actor_id_2: int
    Returns:
        Returns a tuple of tuples, where successive inner tuples have forms (aid_1, aid_2, film_id_1),
        (aid2, aid3, film_id_2), (aid3, aid4, film_id_3), and so on.
    """
    goal_test_fn = lambda actor_id: actor_id == actor_id_2
    return actor_to_goal_path_with_films(transformed_data, actor_id_1, goal_test_fn)


def actor_to_goal_path_with_films(transformed_data, actor_id, goal_test_fn):
    """
    Returns a shortest path from actor_id_1 to the first actor_id for which goal_test_fn returns
    True when passed the actor_id as an argument.

    Args:
        transformed_data:
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
        actor_id_1: int
        goal_test_fn: actor_id -> bool
    Returns:
        Returns a tuple of tuples, where successive inner tuples have forms (aid_1, aid_2, film_id_1),
        (aid2, aid3, film_id_2), (aid3, aid4, film_id_3), and so on, representing a chain of "acted together
        in the same film" relationships between two actors.
        If a path is not found, returns None.
    """
    return actors_to_goal_path_with_films(transformed_data, [actor_id], goal_test_fn)


def actors_to_goal_path_with_films(transformed_data, actor_ids, goal_test_fn):
    """
    Returns a shortest path from any of actor_ids to the first actor_id for which goal_test_fn returns
    True when passed the actor_id as an argument.

    Args:
        transformed data:
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
        actor_ids: list of int
        goal_test_fn: actor_id -> bool
    Returns:
        Returns a tuple of tuples, where successive inner tuples have forms (aid_1, aid_2, film_id_1),
        (aid2, aid3, film_id_2), (aid3, aid4, film_id_3), and so on, representing a chain of "acted together
        in the same film" relationships between two actors.
        If a path is not found, returns None.
    """
    if actor_ids == None:
        return None

    for actor_id in actor_ids:
        if goal_test_fn(actor_id):
            return ((None, actor_id, None),)

    visited = {actor_id for actor_id in actor_ids}

    paths = [((None, actor_id, None),) for actor_id in actor_ids]

    while paths:
        new_paths = []

        for path in paths:
            last_id_in_path = path[-1][1]

            # get potential next actors to add to path
            acted_with = transformed_data["actors"][last_id_in_path]

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


# dictionary { movie_name: movie_id }
with open("resources/movies.pickle", "rb") as f:
    movies_db = pickle.load(f)

# dictionary { movie_id: movie_name }
movie_id_to_name = {v: k for k, v in movies_db.items()}

# dictionary { actor_name: actor_id }
with open("resources/names.pickle", "rb") as f:
    names = pickle.load(f)


def actor_to_actor_film_path(transformed_data, actor_1, actor_2):
    """
    Returns a tuple containing lists of movies, where each list contains the movies that two
    actors acted together in. These actors are part of a shortest path of actors between actor 1
    and actor 2.

    Args:
        transformed_data
            {
                actors: { actor_id: { actor_id: [film_ids]} },
                films: { film_id: [actor_ids]}
            }
        actor_1: string representing actor name or int representing actor_id
        actor_2: string representing actor name or int representing actor_id
    Computes a path of actors between actor_1 and actor 2 based on "acted together" relationships.
    Returns a tuple of lists, where list i represents all movies that actors at positions i-1 and i
    acted together in.

    """
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


def actors_connecting_films(transformed_data, film_id_1, film_id_2):
    actors_in_film_1 = transformed_data["films"].setdefault(film_id_1, None)
    actors_in_film_2 = transformed_data["films"].setdefault(film_id_2, None)

    def goal_test_fn(actor_id):
        return actor_id in actors_in_film_2

    path = actors_to_goal_path_with_films(
        transformed_data, actors_in_film_1, goal_test_fn
    )

    return [item[1] for item in path] if path is not None else None


# HELPERS


def verify_path(transformed_data, path):
    return (
        sum(
            [
                path[i + 1] in transformed_data["actors"][actor_id]
                for i, actor_id in enumerate(path[0:-1])
            ]
        )
        == len(path) - 1
    )


if __name__ == "__main__":
    with open("resources/tiny.pickle", "rb") as f:
        tiny_db = pickle.load(f)

    with open("resources/small.pickle", "rb") as f:
        small_db = pickle.load(f)

    with open("resources/large.pickle", "rb") as f:
        large_db = pickle.load(f)

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
