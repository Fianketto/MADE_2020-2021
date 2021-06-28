import sys
from random import randint, shuffle

MAX_OPERATION_COUNT = pow(10, 6)


class Node:
    def __init__(self, k, y):
        self.key = k
        self.y = y
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def get_key(self, v):
        return 0 if v is None else v.key

    def insert(self, v, k, y):
        t1, t2 = self.split(v, k)
        t3 = self.merge(t1, Node(k, y))
        t1 = self.merge(t3, t2)
        return t1

    def exists(self, v, k):
        if v is None:
            return None
        elif v.key == k:
            return v
        elif v.key > k:
            return self.exists(v.left, k)
        else:
            return self.exists(v.right, k)

    def existing_response(self, v, k):
        res = self.exists(v, k)
        if res is None:
            return "false"
        return "true"

    def delete(self, v, k):
        t1, t2 = self.split(v, k)
        t11, t12 = self.split(t1, k - 1)
        t1 = self.merge(t11, t2)
        return t1

    def next(self, v, k):
        res = None
        while v is not None:
            if v.key > k:
                res = v
                v = v.left
            else:
                v = v.right
        if res is None:
            return "none"
        return str(res.key)

    def prev(self, v, k):
        res = None
        while v is not None:
            if v.key < k:
                res = v
                v = v.right
            else:
                v = v.left
        if res is None:
            return "none"
        return str(res.key)

    def split(self, v, k):
        if v is None:
            return None, None
        if self.get_key(v) > k:
            t1, t2 = self.split(v.left, k)
            v.left = t2
            return t1, v
        else:
            t1, t2 = self.split(v.right, k)
            v.right = t1
            return v, t2

    def merge(self, t1, t2):
        if t1 is None:
            return t2
        if t2 is None:
            return t1
        if t1.y > t2.y:
            t1.right = self.merge(t1.right, t2)
            return t1
        else:
            t2.left = self.merge(t1, t2.left)
            return t2


priority = [i + 1 for i in range(MAX_OPERATION_COUNT)]
shuffle(priority)

bt = BinaryTree()
ans = []
i = 0

for line in sys.stdin.buffer.read().decode().splitlines():
    op, x = list(line.split())
    if op == "insert":
        bt.root = bt.insert(bt.root, int(x), priority[i])
    elif op == "delete":
        bt.root = bt.delete(bt.root, int(x))
    elif op == "exists":
        ans.append(bt.existing_response(bt.root, int(x)))
    elif op == "next":
        ans.append(bt.next(bt.root, int(x)))
    elif op == "prev":
        ans.append(bt.prev(bt.root, int(x)))
    i += 1

sys.stdout.buffer.write("\n".join(ans).encode())

'''
operations = ["insert", "delete", "exists", "next", "prev"]
i = 0
j = 0
for m in range(1000000):
    #op, x = list(input().split())
    op = operations[randint(0, 4)]
    x = randint(-10, 10)
    print(f">>\t{op} {x}")
    if op == "insert":
        bt.root = bt.insert(bt.root, int(x), priority[i])
    elif op == "delete":
        bt.root = bt.delete(bt.root, int(x))
    elif op == "exists":
        ans.append(bt.existing_response(bt.root, int(x)))
        print(ans[j])
        j += 1
    elif op == "next":
        ans.append(bt.next(bt.root, int(x)))
        print(ans[j])
        j += 1
    elif op == "prev":
        ans.append(bt.prev(bt.root, int(x)))
        print(ans[j])
        j += 1
    i += 1
'''
