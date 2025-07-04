"""
6.101
SAT Optional Practice Exercises: Pigeons
"""

# no imports allowed!


def assign_cities(pigeons, destinations):
    """
    Assign carrier pigeons to deliver messages to the given destinations.

    Parameters:
        * pigeons: a list of tuples, where each tuple contains a string
          representing a pigeon's name, and a set of strings representing the
          cities the pigeon can fly to.  Each pigeon has a unique name and
          can deliver at most one message to a destination.

        * destinations: a list of strings representing the destinations of the
          messages that need to be delivered.  Note that a destination may
          appear more than once, meaning that multiple messages have the same
          destination.

    Returns:
        A dictionary mapping pigeon names to the city where they are delivering
        a message.  Pigeons who are not making a delivery should not be
        included.  If no such mapping exists, return None.

    For example:
        * assign_cities([('bob', {'NYC'})], ['IAD'])
            should return None because there are no pigeons that can fly to
            IAD.

        * assign_cities(
            [('dove', {'NYC', 'BOS'}), ('thor', {'NYC', 'BUO'}), ('lily', {'SVY'})],
            ['NYC', 'NYC']
        )
            should return {'dove': 'NYC', 'thor': 'NYC'}.
    """
    raise NotImplementedError


def lottery(prairie_dogs, capacities):
    """
    Assign prairie dogs to live in their preferred burrows without exceeding
    the burrow capacities.

    Parameters:
        * prairie_dogs: a list of lists, where the inner list at index i
          contains integers representing the indices of the burrows that
          prairie dog i would like to live in.

        * capacities: a list of integers representing how many prairie dogs
          can be assigned to the burrow at that index.

    Returns:
        A list of burrow indices, where the element at index i represents 
        the burrow that prairie_dogs[i] was assigned to live in.

    For example:
        * lottery([[0, 1], [1, 0], [0, 1]], [1, 1]) should return None.

        * lottery([[0, 1], [2, 3], [4, 5], [0], [2], [4]], [1, 1, 1, 1, 1, 1])
            should return [1, 3, 5, 0, 2, 4].
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Your code below:
    pass
