import lab


def test_traverse_number():
    s = "def f(x):\n\tnum = 500\nwhile num>0:\nnum -= 10\nreturn num"
    i = s.index("500")
    result = lab.traverse_number(s, i)
    expected = (20, "500")
    assert result == expected


def test_traverse_variable():

    s = "def f(x):\n\tnum = 500\nwhile num>0:\nnum -= 10\nreturn num"
    i = s.index("num")
    result = lab.traverse_variable(s, i)
    expected = (14, "num")
    assert result == expected
