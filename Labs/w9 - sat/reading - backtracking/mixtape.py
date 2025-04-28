def mixtape_agenda(songs, target_duration):
    agenda = [set()]
    visited = set()
    while agenda:
        this_mixtape = agenda.pop()
        if this_mixtape in visited:
            continue
        visited.add(frozenset(this_mixtape))

        duration = sum(songs[s] for s in this_mixtape)
        if duration == target_duration:
            return this_mixtape
        if duration > target_duration:
            continue
        for song in songs:
            if song not in this_mixtape:
                agenda.append(this_mixtape | {song})
    return None


def mixtape(songs, target_duration):
    """
    Given a dictionary of songs (mapping titles to durations), as well as a
    total target duration, return a set of song titles such that the sum of
    those songs' durations equals the target_duration.

    If no such set exists, return None instead.

    >>> songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
    >>> mixtape(songs, 21) == {'A', 'B', 'C'}
    True
    >>> mixtape(songs, 1000) is None
    True
    """
    if target_duration == 0:
        return set()

    if target_duration < 0 or not songs:
        return None

    song = list(songs.keys())[0]
    songs_rest = {k: v for k, v in songs.items() if k != song}
    duration = songs[song]

    # if the first song is part of a solution, we can fill the remaining space
    # on the tape with other songs
    recursive_result1 = mixtape(songs_rest, target_duration - duration)
    if recursive_result1 is not None:
        return {song} | recursive_result1

    # if the first song is not part of the solution, we should try to fill the
    # whole duration with other songs.
    recursive_result2 = mixtape(songs_rest, target_duration)
    if recursive_result2 is not None:
        return recursive_result2

    # if there is no solution with the first song, and no solution without it,
    # then there must be no solution.
    return None


def mixtape2(songs, target_duration):
    if target_duration == 0:
        return set()

    if not songs or target_duration < 0:
        return None

    for song, duration in songs.items():
        recursive_result = mixtape(
            {k: v for k, v in songs.items() if k != song}, target_duration - duration
        )

        if recursive_result is not None:
            return {song} | recursive_result

    return None


def mixtape3(songs, target_duration, so_far=frozenset()):
    so_far_duration = sum(songs[s] for s in so_far)
    if so_far_duration == target_duration:
        return so_far

    if so_far_duration > target_duration:
        return None

    for song in list(songs):
        if song in so_far:
            continue
        recursive_result = mixtape3(songs, target_duration, so_far | {song})
        if recursive_result is not None:
            return recursive_result

    return None


import time

if __name__ == "__main__":
    import doctest

    doctest.testmod()

    songs = {"A": 5, "B": 10, "C": 6, "D": 2}
    t0 = time.time()
    r1 = mixtape_agenda(songs, 21)
    t1 = time.time()
    r2 = mixtape(songs, 21)
    t2 = time.time()
    r3 = mixtape2(songs, 21)
    t3 = time.time()
    r4 = mixtape3(songs, 21)
    t4 = time.time()

    print(f"{t1-t0}, {t2-t1}, {t3-t2}, {t4-t3}")

    print(r1, r2, r3, r4)
