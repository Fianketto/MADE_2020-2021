import sys


class Vector:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.begin = 0
        self.end = 0
        self.elements = [0]

    def pop(self):
        if self.size == 0:
            return None
        first_element = self.elements[self.begin]
        self.size -= 1
        self.begin = (self.begin + 1) % self.capacity
        self.ensure_capacity()
        return first_element

    def push(self, x):
        self.ensure_capacity()
        self.size += 1
        self.end = (self.end + 1) % self.capacity
        self.elements[self.end] = x

    def ensure_capacity(self):
        if self.size < self.capacity // 4:
            elements_new = ['' for i in range(self.capacity // 2)]
            for i in range(self.size):
                elements_new[i] = self.elements[(self.begin + i) % self.capacity]
            self.elements = elements_new
            self.capacity //= 2
            self.begin = 0
            self.end = self.size - 1
        elif self.size == self.capacity:
            elements_new = ['' for i in range(self.capacity * 2)]
            for i in range(self.size):
                elements_new[i] = self.elements[(self.begin + i) % self.capacity]
            self.elements = elements_new
            self.capacity *= 2
            self.begin = 0
            self.end = self.size - 1


v = Vector()
n = int(sys.stdin.readline())
for i in range(n):
    a = list(sys.stdin.readline().split())
    if a[0] == '+':
        v.push(int(a[1]))
    else:
        sys.stdout.write(str(v.pop()) + "\n")

"""
print(v.elements, "\tsize:", v.size, "/", v.capacity, "\tbegin and end:", v.begin, v.end)
for i in range(100):
    a = list(map(int, input().split()))
    if a[0] == 1:
        v.push(a[1])
    else:
        v.pop()
    print(v.elements, "\tsize:", v.size, "/", v.capacity, "\tbegin and end:", v.begin, v.end)
"""
