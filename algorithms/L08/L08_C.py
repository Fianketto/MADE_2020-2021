import sys


class Node:
    def __init__(self, k):
        self.key = k
        self.h = 0
        self.node_count_on_the_right = 0
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
        print("rot right")
        q = v.left
        v.left = q.right
        q.right = v
        q.node_count_on_the_right += 1 + v.node_count_on_the_right
        self.fix(v)
        self.fix(q)
        return q

    def rotate_left(self, v):
        print("rot left")
        p = v.right
        v.right = p.left
        p.left = v
        v.node_count_on_the_right -= (1 + p.node_count_on_the_right)
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
            v.node_count_on_the_right += 1
            v.right = self.insert(v.right, k)
        return self.balance(v)

    def delete(self, v, k):
        if v is None:
            return None
        elif v.key > k:
            v.left = self.delete(v.left, k)
        elif v.key < k:
            v.node_count_on_the_right -= 1
            v.right = self.delete(v.right, k)
        else:
            q = v.left
            r = v.right
            if r is None:
                return q
            min_node = self.find_min(r)
            min_node.right = self.delete_min(r)
            min_node.left = q
            min_node.node_count_on_the_right = v.node_count_on_the_right - 1
            return self.balance(min_node)
        return self.balance(v)

    def find_min(self, v):
        while v.left is not None:
            v = v.left
        return v

    def delete_min(self, v):
        if v.left is None:
            return v.right
        v.left = self.delete_min(v.left)
        return self.balance(v)

    def print_tree(self, v):
        if v is not None:
            self.print_tree(v.left)
            print(v.key, end=" ")
            self.print_tree(v.right)

    def get_k_max(self, v, k):
        if v.node_count_on_the_right == k - 1:
            return str(v.key)
        elif v.node_count_on_the_right >= k:
            return self.get_k_max(v.right, k)
        else:
            return self.get_k_max(v.left, k - v.node_count_on_the_right - 1)


bt = BinaryTree()
ans = []
n = int(sys.stdin.buffer.readline().decode())
for line in sys.stdin.buffer.read().decode().splitlines():
    op, x = list(line.split())
    if op[0] == "-":
        bt.root = bt.delete(bt.root, int(x))
    elif op[0] == "0":
        ans.append(bt.get_k_max(bt.root, int(x)))
    else:
        bt.root = bt.insert(bt.root, int(x))

sys.stdout.buffer.write("\n".join(ans).encode())
