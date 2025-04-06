# 6.101 recitation: lab 2 midpoint


############### Creating and calling a function


def foo(x):
    return 3 * x**4

foo(3)












############### Taking derivative of a function

def foo(x):
    return 3 * x**4

def deriv(f, dx=0.001):
    """
    Given a function f of one variable (which takes a float value and returns a float value)
    returns a function that approximates the derivative df/dx.

    Optional parameter dx > 0 is the width of the approximation (the true derivative is the limit as dx -> 0).
    """
    def fprime(x):
        ________   # df/dx evaluated at x (using dx)
    return ________

dfoo = deriv(foo) # => function approximately equal to ________

dfoo(3)

ddfoo = deriv(dfoo) # => function approximately equal to _______










############### Comparing our approximate derivative with true derivative

def foo(x):
    return 3 * x**4
dfoo = deriv(foo) # approximately 12x^3
ddfoo = deriv(dfoo) # approximately 36x^2

def compare(f, g, x_values):
    for x in x_values:
        print(f'{x=} {f(x)=} {g(x)=}')

# compare(dfoo, 12 * x**3, range(-10, 10))

# compare(ddfoo, 36 * x**2, range(-10, 10))








############### nth derivatives

def nth_derivative(f, n):
    """
    Given a function f of one variable (takes a float value and returns a float value)
    returns a function that approximates the nth derivative of f.
    """
    g = f
    for _ in range(n):
        __________
    return g

h = nth_derivative(lambda x: x**5, 3) # => third derivative of x^5 = 60x^2
