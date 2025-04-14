# 6.101 recitation: Bacon wrapup

####################### data representations

# raw data:
# [
#     ( actor1, actor2, film ),
#     ...
# ]

# key operation for our graph search is *neighbors*:
# given an actor, which actors appeared with that actor?

def get_neighbors(data, actor):
    pass














# transformed data:
# {
#     actor1: {actor2, ...},
#     actor2: {actor1, ...},
#     ...
# }

# what does the neighbors operation look like now?

def get_neighbors(data, actor):
    pass


# what are we missing from this rep?








####################### refactoring

# what's good?
# what to improve?
# buggy?


def transform_data(raw_data):
    return raw_data


def bacon_path(transformed_data, actor_id):
    """
    bacon path
    """
    agenda = [(4724,)]
    visited = [(4724,)]

    while agenda:
        p = agenda.pop(0)
        a = p[-1]
        if a == actor_id:
            return p

        for n in [x[1] for x in transformed_data if x[0] == a]:
            nn = p + (n,)
            agenda.append(nn)
            visited.append(nn)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Given a database from transform_data(), return a shortest path of actors
    from actor 1 to actor 2 as a list.
    """
    raise NotImplementedError


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Given a database from transform_data(), return a shortest path of actors
    starting from actor 1 until reaching an actor who satisfies
    goal_test_function (which takes an actor and returns a truthy value).
    """
    raise NotImplementedError


def film_path(transformed_data, actor_id_1, actor_id_2):
    """
    Given a database from transform_data(),
    return a shortest path of film ids that connect actor 1 to actor 2.
    """
    raise NotImplementedError


def actors_connecting_films(transformed_data, film1, film2):
    """
    Given a database from transform_data(),
    return a shortest path of actors that connect film1 to film2.
    """
    raise NotImplementedError
