# 6.101 recitation: lab 3 wrapup


####################### data representations

# raw data:
[
    ( actor1, actor2, film )
    ...
]

# key operation for our graph search is *neighbors*:
# given an actor, which actors appeared with that actor?
















# transformed data:
{
    actor1: set(actor2, ...)
    actor2: set(actor1, ...)
    ...
}

# what does the neighbors operation look like now?

# what are we missing from this rep?








####################### refactoring

# what's good?
# what to improve?
# buggy?

def bacon_path(transformed_data, actor_id):
    """
    bacon path
    """
    agenda = [(4724,)]
    visited = [(4724,)]
    ... # 20 lines of path-finding code from reading, using actor_id as the goal

def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Given a database from transform_data(),
    return a shortest path of actors from actor 1 to actor 2 as a list.
    """
    agenda = [(actor_id_1,)]
    visited = [(actor_id_1,)]
    ... # same 20 lines of path-finding code from reading, using actor_id_2 as the goal









def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Given a database from transform_data(),
    return a shortest path of actors starting from actor 1 until reaching an actor who
    satisfies goal_test_function (which takes an actor and returns a truthy value).
    """
    ... # path-finding code using actor_id_1 as start and goal_test_function(actor) as the stopping criterion








def film_path(transformed_data, actor_id_1, actor_id_2):
    """
    Given a database from transform_data(),
    return a shortest path of film ids that connect actor 1 to actor 2.
    """
    ...

def actors_connecting_films(transformed_data, film1, film2):
    """
    Given a database from transform_data(),
    return a shortest path of actors that connect film1 to film2.
    """
    ...








