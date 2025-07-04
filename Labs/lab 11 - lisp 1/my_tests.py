import lab
import pytest


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


def test_calc_mul():
    assert lab.calc_mul() == 1
    assert lab.calc_mul(1, 2) == 2
    assert lab.calc_mul(1, 2, 3, 4, 5) == 120


def test_calc_div():
    with pytest.raises(TypeError):
        lab.calc_div()
    assert lab.calc_div(1, 2) == 0.5
    assert lab.calc_div(1, 2, 3) == pytest.approx(0.166666666666)
