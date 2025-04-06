functions = []


def outer(i):
    def func(x):
        return x + i

    return func


for i in range(5):
    functions.append(outer(i))


def make_adder(i):
    return lambda x: x + i


if __name__ == "__main__":
    import sys

    increment_value = int(sys.argv[1])

    for f in functions:
        print(f(increment_value))
