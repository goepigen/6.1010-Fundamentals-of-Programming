class Vector2D:
    ndims = 2

    def magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5


class Node:
    def __init__(self, element, next_node=None):
        self.element = element
        self.next_node = next_node

    # def __iter__(self):
    #     yield self.element
    #     if self.next_node:
    #         yield from self.next_node


class LinkedList:
    def __init__(self, iterable=None):
        self.head = None
        if iterable:
            iterator = iter(iterable)
            self.head = Node(next(iterator))
            current = self.head
            for element in iterator:
                current.next_node = Node(element)
                current = current.next_node

    def append(self, element):
        if self.head is None:
            self.head = Node(element)
        else:
            current = self.head
            while current.next_node:
                current = current.next_node
            current.next_node = Node(element)

    def _get_node(self, index):
        if index == 0:
            return self
        elif self.next_node is None:
            raise IndexError("Index is out of range")
        else:
            return self.next_node._get_node(index - 1)

    def __getitem__(self, index):
        return self._get_node(index).element

    def __setitem__(self, index, value):
        self._get_node(index).element = value

    def __str__(self):
        return "LinkedList([" + ", ".join(map(str, self)) + "])"

    def __len__(self):
        # Iterative Version
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next_node
        return count

        # Recursive Version
        # current = self.head
        # if self.head == 0:
        #     return 0
        # return 1 + len(current.next_node)

    def __iter__(self):
        # Iterative Version
        current = self.head
        while current is not None:
            yield current.element
            current = current.next_node

        # Recursive Version - requires Node to implement __iter__()
        # if self.head:
        #     yield from self.head

    def copy(self):
        new_list = LinkedList()
        for item in self:
            new_list.append(item)
        return new_list

    def __delitem__(self, index):
        if index == 0:
            if self.head is None:
                raise IndexError("Deletion from empty list")
            self.head = self.head.next_node
        else:
            prev = self._get_node(index - 1)
            node = prev.next_node
            if node is None:
                raise IndexError("Index out of range")
            prev.next_node = node.next_node

    def __add__(self, other):
        if not isinstance(other, LinkedList):
            return NotImplemented

        result = self.copy()
        for item in other:
            result.append(item)

        return result

    def insert(self, index, element):
        if index < 0 or index > len(self):
            raise IndexError("Index out of range")

        new_node = Node(element)

        if index == 0:
            new_node.next_node = self.head
            self.head = new_node
            return

        current = self.head
        count = 0
        while current.next_node and count < index - 1:
            current = current.next_node
            count += 1

        new_node = Node(element)
        new_node.next_node = current.next_node
        current.next_node = new_node


x = LinkedList([8, 15, 16, 23, 42])


print(len(x))
