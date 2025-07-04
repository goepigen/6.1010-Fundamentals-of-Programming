"""
6.1010 Spring 2023
Lab10 Optional Practice Exercises: Match
"""

import doctest


class Dot():
    """
    Matches any single character at the beginning of a piece of text.
    Does not match the empty string.
    """
    def match(self, text):
        if text:
            return text[0]
        

class Verbatim():
    """
    Matches the given string, verbatim, at the beginning of a piece of text.
    """
    def __init__(self, string):
        self.string = string

    def match(self, text):
        subseq = text[:len(self.string)]
        if self.string == subseq:
            return subseq

class CharFrom():
    """
    Matches any single character from the given iterable object of characters.
    """
    def __init__(self, chars):
        raise NotImplementedError

    def match(self, text):
        raise NotImplementedError
    
class Digit():
    """
    Matches any single integer digit 0-9.
    """
    def __init__(self):
        raise NotImplementedError

    def match(self, text):
        raise NotImplementedError

class Sequence():
    """
    Matches only if the given patterns all occur in order.  Patterns is given
    as a list of instances of one of these classes.
    """
    def __init__(self, patterns):
        self.patterns = patterns

    def match(self, text):
        cur_result = ''
        for pattern in self.patterns:
            result = pattern.match(text[len(cur_result):])
            if result is not None:
                cur_result += result
            else: 
                return None
        return cur_result


class Alternatives():
    """
    Matches if _any_ of the given patterns match, by trying them in the order
    they were given.
    """
    def __init__(self, patterns):
        raise NotImplementedError

    def match(self, text):
        raise NotImplementedError


class Repeat():
    """
    Matches if the given pattern (given as an instance of one of these classes)
    exists repeated between n_min (inclusive) and n_max (inclusive) times.
    This matching should be greedy (i.e., it should match as many repetitions
    as possible up to `n_max` times).  It should not match if there are fewer
    than `n_min` repetitions.
    """
    def __init__(self, pattern, n_min, n_max):
        raise NotImplementedError

    def match(self, text):
        raise NotImplementedError
    

class Number():
    """
    Matches if the text matches one or more consecutive digits (no limit).
    This matching should be greedy (i.e., it should match as many consecutive
    digits as possible).  It should not match if there is not a digit at the 
    given location.
    """
    def __init__(self):
        raise NotImplementedError

    def match(self, text):
        raise NotImplementedError


class Star():
    """
    Matches the given pattern (an instance of one of these classes) repeated an
    arbitrary number of times.  0 times (matching the empty string) is a valid
    match.
    """
    def __init__(self, pattern):
        raise NotImplementedError

    def match(self, text):
        raise NotImplementedError


if __name__ == "__main__":
    doctest.testmod()
