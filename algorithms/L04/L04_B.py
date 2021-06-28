import sys


class Vector:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.elements = [0]

    def pop(self):
        if self.size == 0:
            return None
        last_element = self.elements[self.size - 1]
        self.size -= 1
        self.ensure_capacity()
        return last_element

    def push(self, x):
        self.ensure_capacity()
        self.size += 1
        self.elements[self.size - 1] = x

    def ensure_capacity(self):
        if self.size < self.capacity // 4:
            elements_new = ['' for i in range(self.capacity // 2)]
            for i in range(self.size):
                elements_new[i] = self.elements[i]
            self.elements = elements_new
            self.capacity //= 2
        elif self.size == self.capacity:
            elements_new = ['' for i in range(self.capacity * 2)]
            for i in range(self.size):
                elements_new[i] = self.elements[i]
            self.elements = elements_new
            self.capacity *= 2


def evaluate_operation(op, x, y):
    if op == "+":
        return y + x
    elif op == "-":
        return y - x
    elif op == "*":
        return y * x


v = Vector()
arr = list(sys.stdin.readline().split())
for i in range(len(arr)):
    if arr[i] not in ('+', '-', '*'):
        v.push(int(arr[i]))
    else:
        x = v.pop()
        y = v.pop()
        v.push(evaluate_operation(arr[i], x, y))

sys.stdout.write(str(v.pop()) + "\n")
