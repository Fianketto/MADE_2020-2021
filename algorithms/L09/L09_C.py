import sys
from random import randint, shuffle

MAX_OPERATION_COUNT = pow(10, 5)


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 1
        self.left = None
        self.right = None


class TreapTree:
    def __init__(self):
        self.root = None
        self.all_values = []
        self.iter = 0

    def save_all_values(self):
        if self.root is not None:
            self.all_values = [0 for i in range(self.get_size(self.root))]
            self.get_all_values(self.root)

    def get_all_values(self, v):
        if v is not None:
            if v.left is not None:
                self.get_all_values(v.left)
            self.all_values[self.iter] = str(v.x)
            self.iter += 1
            self.get_all_values(v.right)

    def get_size(self, v):
        return 0 if v is None else v.size

    def fix_size(self, v):
        v.size = self.get_size(v.left) + self.get_size(v.right) + 1

    def insert(self, v, k, x, y):
        t1, t2 = self.split(v, k)
        t3 = self.merge(t1, Node(x, y))
        t1 = self.merge(t3, t2)
        return t1

    def move_to_beginning(self, l, r):
        t1, t2 = self.split(self.root, l - 1)
        t21, t22 = self.split(t2, r - l)
        t = self.merge(t21, t1)
        t = self.merge(t, t22)
        return t

    def split(self, v, k):
        if v is None:
            return None, None
        if self.get_size(v.left) > k:
            t1, t2 = self.split(v.left, k)
            v.left = t2
            self.fix_size(v)
            return t1, v
        else:
            t1, t2 = self.split(v.right, k - self.get_size(v.left) - 1)
            v.right = t1
            self.fix_size(v)
            return v, t2

    def merge(self, t1, t2):
        if t1 is None:
            return t2
        if t2 is None:
            return t1
        if t1.y > t2.y:
            t1.right = self.merge(t1.right, t2)
            self.fix_size(t1)
            return t1
        else:
            t2.left = self.merge(t1, t2.left)
            self.fix_size(t2)
            return t2

    def print_tree(self, v):
        if v is not None:
            self.print_tree(v.left)
            print(v.x, end=" ")
            self.print_tree(v.right)


n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
priority = [i + 1 for i in range(MAX_OPERATION_COUNT)]
shuffle(priority)
tt = TreapTree()
i = 0

for j in range(n):
    tt.root = tt.insert(tt.root, j, j + 1, priority[i])
    i += 1

for line in sys.stdin.buffer.read().decode().splitlines():
    left_border, right_border = list(line.split())
    tt.root = tt.move_to_beginning(int(left_border) - 1, int(right_border) - 1)

tt.save_all_values()
print(" ".join(tt.all_values))
