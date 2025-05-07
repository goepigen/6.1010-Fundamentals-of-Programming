"""
6.101 Lab:
Symbolic Algebra
"""

# import doctest # optional import
# import typing # optional import
# import pprint # optional import
# import string # optional import
# import abc # optional import

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Expr:
    pass


class Var(Expr):
    def __init__(self, name):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"


class Num(Expr):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"


if __name__ == "__main__":
    pass
