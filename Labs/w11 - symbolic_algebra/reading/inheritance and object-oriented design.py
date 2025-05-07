x = "dog"


class A:
    x = "cat"


class B(A):
    x = "ferret"

    def __init__(self):
        # x = "tomato"
        self.x = self.x


class C(B):
    x = "fish"

    def __init__(self):
        pass


# b = B()
# print(b.x)

c = C()
print(c.x)
