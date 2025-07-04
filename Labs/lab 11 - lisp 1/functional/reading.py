def all_caps_list(words):
    if len(words) == 1:
        return [words[0].upper()]
    else:
        return [words[0].upper()] + all_caps_list(words[1:])


# for i in range(n):
#     print('hello', i)


def p_rec(n):
    if n == 1:
        print("hello", n)
    else:
        p_rec(n - 1)
        print("hello", n)


def repeat_n_times(n, func):
    if n == 0:
        return
    func(n)
    repeat_n_times(n - 1, func)


def counter():
    tally = 0

    def increment():
        tally += 1
        return tally

    return increment


def bank():
    accounts = {}

    def balance_of(account):
        return accounts.get(account, 0)

    def deposit(account, amount):
        accounts[account] = balance_of(account) + amount

    return balance_of, deposit


def fib_inefficient(n):
    if n < 2:
        return n
    return fib_inefficient(n - 2) + fib_inefficient(n - 1)


def fib(n):
    cache = {}

    def _actual_fib(n):
        if n not in cache:
            if n < 2:
                cache[n] = n
            else:
                cache[n] = _actual_fib(n - 2) + _actual_fib(n - 1)
        return cache[n]

    return _actual_fib(n)


class MemoizedFunction:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]


def memoize(func):
    cache = {}

    def _memoized_func(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return _memoized_func


@memoize
def fib_inefficient2(n):
    if n < 2:
        return n
    return fib_inefficient2(n - 2) + fib_inefficient2(n - 1)


if __name__ == "__main__":
    # print(all_caps_list(["damn", "man"]))
    # p_rec(4)
    # repeat_n_times(4, lambda i: print("hello", i))

    inc = counter()
    # inc()    error because no use of nonlocal on tally

    # balance_of, deposit = bank()

    # print(balance_of("me"))
    # print(deposit("me", 1000))
    # print(balance_of("me"))
    # print(fib(100))

    # fib_inefficient = MemoizedFunction(fib_inefficient)

    # fib_inefficient = memoize(fib_inefficient)
    # print(fib_inefficient.__call__(100))

    print(fib_inefficient2.__call__(100))
