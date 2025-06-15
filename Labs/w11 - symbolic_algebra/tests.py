import lab


def test_print_binop():
    expr1 = lab.Add("x", 3)
    assert str(expr1) == "x + 3"

    expr2 = lab.Mul(expr1, 5)
    assert str(expr2) == "(x + 3) * 5"

    expr3 = lab.Div(expr1, expr2)
    assert str(expr3) == "(x + 3) / ((x + 3) * 5)"

    expr4 = lab.Sub("x", expr1)
    assert str(expr4) == "x - (x + 3)"


def test_python_operators():
    x = lab.Var("x")
    y = lab.Var("y")

    assert str(x + y) == str(lab.Add(x, y))
    assert str(2 + x) == str(lab.Add(2, x))
    assert str(2 + x + y) == str(lab.Add(2, lab.Add(x, y)))

    assert str(x - y) == str(lab.Sub(x, y))
    assert str(2 - x) == str(lab.Sub(2, x))

    assert str(2 - x + y) == str(lab.Add(lab.Sub(2, x), y))

    assert str(2 * x + y) == str(lab.Add(lab.Mul(2, x), y))

    assert str(2 / x + y) == str(lab.Add(lab.Div(2, x), y))
