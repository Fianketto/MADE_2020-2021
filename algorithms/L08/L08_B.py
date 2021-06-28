import sys


class Node:
    def __init__(self, k):
        self.key = k
        self.h = 0
        self.balance = 0
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def get_height(self, v):
        return 0 if v is None else v.h

    def get_key(self, v):
        return 0 if v is None else v.key

    def get_balance(self, v):
        return self.get_height(v.right) - self.get_height(v.left)

    def fix(self, v):
        h1 = self.get_height(v.left)
        h2 = self.get_height(v.right)
        v.h = max(h1, h2) + 1

    def rotate_right(self, v):
        q = v.left
        v.left = q.right
        q.right = v
        self.fix(v)
        self.fix(q)
        return q

    def rotate_left(self, v):
        p = v.right
        v.right = p.left
        p.left = v
        self.fix(v)
        self.fix(p)
        return p

    def balance(self, v):
        self.fix(v)
        if self.get_balance(v) == 2:
            if self.get_balance(v.right) < 0:
                v.right = self.rotate_right(v.right)
            return self.rotate_left(v)
        if self.get_balance(v) == -2:
            if self.get_balance(v.left) > 0:
                v.left = self.rotate_left(v.left)
            return self.rotate_right(v)
        return v

    def insert(self, v, k):
        if v is None:
            return Node(k)
        elif k < v.key:
            v.left = self.insert(v.left, k)
        elif k > v.key:
            v.right = self.insert(v.right, k)
        return self.balance(v)

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
        if v is None:
            return None
        elif v.key > k:
            v.left = self.delete(v.left, k)
        elif v.key < k:
            v.right = self.delete(v.right, k)
        else:
            q = v.left
            r = v.right
            if r is None:
                return q
            min_node = self.find_min(r)
            min_node.right = self.delete_min(r)
            min_node.left = q
            return self.balance(min_node)
        return self.balance(v)

    def find_max(self, v):
        while v.right is not None:
            v = v.right
        return v

    def find_min(self, v):
        while v.left is not None:
            v = v.left
        return v

    def delete_min(self, v):
        if v.left is None:
            return v.right
        v.left = self.delete_min(v.left)
        return self.balance(v)

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


bt = BinaryTree()
ans = []
for line in sys.stdin.buffer.read().decode().splitlines():
    op, x = list(line.split())
    if op == "insert":
        bt.root = bt.insert(bt.root, int(x))
    elif op == "delete":
        bt.root = bt.delete(bt.root, int(x))
    elif op == "exists":
        ans.append(bt.existing_response(bt.root, int(x)))
    elif op == "next":
        ans.append(bt.next(bt.root, int(x)))
    elif op == "prev":
        ans.append(bt.prev(bt.root, int(x)))

sys.stdout.buffer.write("\n".join(ans).encode())
