class MyObj:
    pass


m = MyObj()


def test():
    """
    >>> test()    # doctest: +ELLIPSIS
    '<t.MyObj object at 0x...>'
    """
    return repr(m)
