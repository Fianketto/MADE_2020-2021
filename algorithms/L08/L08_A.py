import sys


class Node:
    def __init__(self, k):
        self.key = k
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, v, k):
        if v is None:
            return Node(k)
        elif k < v.key:
            v.left = self.insert(v.left, k)
        elif k > v.key:
            v.right = self.insert(v.right, k)
        return v

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
            if v.left is None:
                v = v.right
            elif v.right is None:
                v = v.left
            else:
                v.key = self.find_max(v.left).key
                v.left = self.delete(v.left, v.key)
        return v

    def find_max(self, v):
        while v.right is not None:
            v = v.right
        return v

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
