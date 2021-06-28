import sys
from random import randint, shuffle


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 1
        self.is_reversed = False
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
            self.check_reversion(v)
            if v.left is not None:
                self.get_all_values(v.left)
            self.all_values[self.iter] = str(v.x)
            self.iter += 1
            self.get_all_values(v.right)

    def get_size(self, v):
        return 0 if v is None else v.size

    def fix_size(self, v):
        v.size = self.get_size(v.left) + self.get_size(v.right) + 1

    def reverse(self, l, r):
        t1, t2 = self.split(self.root, l - 1)
        self.check_reversion(t1)
        self.check_reversion(t2)
        t21, t22 = self.split(t2, r - l)
        t21.is_reversed = True
        t = self.merge(t1, t21)
        t = self.merge(t, t22)
        self.root = t

    def check_reversion(self, v):
        if v is not None and v.is_reversed:
            self.apply_reversion(v)

    def apply_reversion(self, v):
        v.is_reversed = False
        self.swap_children(v)
        self.mark_children_as_reversed(v)

    def swap_children(self, v):
        v.left, v.right = v.right, v.left

    def mark_children_as_reversed(self, v):
        if v.left is not None:
            v.left.is_reversed = not v.left.is_reversed
        if v.right is not None:
            v.right.is_reversed = not v.right.is_reversed

    def insert(self, v, k, x, y):
        t1, t2 = self.split(v, k)
        t3 = self.merge(t1, Node(x, y))
        t1 = self.merge(t3, t2)
        return t1

    def split(self, v, k):
        if v is None:
            return None, None
        self.check_reversion(v)
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
        self.check_reversion(t1)
        self.check_reversion(t2)
        if t1.y > t2.y:
            t1.right = self.merge(t1.right, t2)
            self.fix_size(t1)
            return t1
        else:
            t2.left = self.merge(t1, t2.left)
            self.fix_size(t2)
            return t2


n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
priority = [i + 1 for i in range(n)]
shuffle(priority)
tt = TreapTree()
i = 0

for j in range(n):
    tt.root = tt.insert(tt.root, j, j + 1, priority[i])
    i += 1

for line in sys.stdin.buffer.read().decode().splitlines():
    left_border, right_border = list(line.split())
    tt.reverse(int(left_border) - 1, int(right_border) - 1)

tt.save_all_values()
print(" ".join(tt.all_values))
