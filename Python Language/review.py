def f1(arg1, arg2):
    print(arg1, arg2)


def list_items(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")


def list_items2(*args):
    for el in args:
        print(el)


def list_items3(arg1, arg2, *args, **kwargs):
    print(arg1, arg2)
    for el in args:
        print(args)
    for k, v in kwargs.items():
        print(k, v)


if __name__ == "__main__":
    d1 = {"arg1": 1, "arg2": 2}

    f1(**d1)

    list_items(name="Horn", age=40)
    list_items2("Horn", 30)
    list_items3("a1", "a2", "a3", "a4", named1="a5", named2="a6")
