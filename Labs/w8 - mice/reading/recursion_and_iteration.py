def factorial_rec(n):
    assert n >= 0, "need a nonnegative integer"
    if n == 0:
        return 1
    else:
        return n * factorial_rec(n - 1)


def factorial_iter(n):
    assert n >= 0, "need a nonnegative integer"
    out = 1
    for i in range(1, n + 1):
        out += i
    return out


def sum_list_iter(x):
    sum_so_far = 0
    for num in x:
        sum_so_far += num
    return sum_so_far


def sum_list_rec(x):
    if not x:
        return 0
    else:
        return x[0] + sum_list_rec(x[1:])


def sum_list_lr(x):
    if not x:
        return 0
    else:
        m = len(x) // 2
        return sum_list_lr(x[0:m]) + sum_list_lr(x[m:])


def sum_list_helper(x):
    def sum_helper(sum_so_far, lst):
        if not lst:
            return sum_so_far
        else:
            num = lst[0]
            rest = lst[1:]
            return sum_helper(sum_so_far + num, rest)

    return sum_helper(0, x)


def sum_nested(x):
    if not x:
        return 0
    elif isinstance(x[0], list):
        return sum_nested(x[0]) + sum_nested(x[1:])
    else:
        return x[0] + sum_nested(x[1:])


def sum_nested_rec(original_x):
    sum_so_far = 0
    agenda = [original_x]
    while agenda:
        x = agenda.pop(-1)
        if not x:
            sum_so_far += 0
        elif isinstance(x[0], list):
            agenda.append(x[0])
            agenda.append(x[1:])
        else:
            sum_so_far += x[0]
            agenda.append(x[1:])
    return sum_so_far


def negate_elements(x):
    out = []
    for val in x:
        out.append(-val)
    return out


def negate_elements_gen(x):
    for val in x:
        yield -val


def all_values(tree):
    agenda = [tree]

    while agenda:
        current = agenda.pop(-1)
        yield current[0]
        agenda.extend(current[1:])
