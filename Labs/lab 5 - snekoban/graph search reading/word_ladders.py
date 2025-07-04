import puzzle15

# ALL_WORDS is a set containing all strings that should be considered valid
# words (all in lower-case)
with open("words.txt") as f:
    ALL_WORDS = {i.strip() for i in f}

alphabet = list("abcdefghijklmnopqrstuvwxyz")


def create_word_ladder_neighbors(word_set, goal):
    """
    takes a state as input
    returns all neighboring states (valid words that differ in one letter)
    """

    goal_length = len(goal)
    reduced_word_set = {w for w in word_set if len(w) == goal_length}

    def word_ladder_neighbors(state):
        word_length = len(state)

        neighbors = []

        for i in range(word_length):
            for new_char in alphabet:
                new_word = state[:i] + new_char + state[i + 1 :]
                if new_word in reduced_word_set:
                    neighbors.append(new_word)

        return tuple(neighbors)

    return word_ladder_neighbors


# replace this goal test function:


if __name__ == "__main__":
    start_state = "patties"
    goal = "foaming"

    def goal_test_function(state):
        """
        takes a state as input
        returns True if and only if state matches the goal (the target word)
        """
        return state == goal

    neighbors_fn = create_word_ladder_neighbors(ALL_WORDS, goal)

    path = puzzle15.find_path(neighbors_fn, start_state, goal_test_function)
