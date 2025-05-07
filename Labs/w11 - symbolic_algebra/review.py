class MyClass1:
    def __iter__(self):
        return iter([1, 2, 3])


# Valid Iterator
class MyClass3:
    def __init__(self, lst):
        self.values = lst
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.pos > len(self.lst):
            raise StopIteration
        next_value = self.values[self.pos]
        self.pos += 1
        return next_value


# Valid Iterable
class MyClass4:
    def __init__(self, lst):
        self.values = lst

    def __iter__(self):
        for x in self.values:
            yield x


# Valid Iterator
class MyClass5:
    def __init__(self, lst):
        self._iterator = iter(lst)

    def __iter__(self):
        self

    def __next__(self):
        return next(self._iterator)


# generator expression version
values = [1, 2, 3, 4]
it = (x for x in values)


class BadCounter:
    def __init__(self):
        self.i = 0

    def __iter__(self):
        return iter([1, 2, 3])

    def __next__(self):
        self.i += 1
        return self.i


breakpoint()
bc = BadCounter()
for i in bc:
    print(i)
