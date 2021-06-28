import sys


class Map:
    def __init__(self):
        self.M = 10 ** 5
        self.P = 2000003
        self.A = 31
        self.arr = [[] for i in range(self.M)]

    def hash_func(self, s):
        res = 0
        for i in range(len(s)):
            res = (res * self.A + ord(s[i])) % self.P
        res %= self.M
        return res

    def put(self, k, v):
        h = self.hash_func(k)
        for i in range(len(self.arr[h])):
            if self.arr[h][i][0] == k:
                self.arr[h][i][1] = v
                return
        self.arr[h].append([k, v])

    def delete(self, k):
        h = self.hash_func(k)
        for i in range(len(self.arr[h])):
            if self.arr[h][i][0] == k:
                del self.arr[h][i]
                return

    def get(self, k):
        h = self.hash_func(k)
        for i in range(len(self.arr[h])):
            if self.arr[h][i][0] == k:
                return self.arr[h][i][1]
        return "none"


m = Map()
ans = []
for line in sys.stdin.buffer.read().decode().splitlines():
    a = list(line.split())
    if a[0][0] == 'p':
        m.put(a[1], a[2])
    elif a[0][0] == 'd':
        m.delete(a[1])
    else:
        # stdout.write(m.get(a[1]) + "\n")
        ans.append(m.get(a[1]))

sys.stdout.buffer.write("\n".join(ans).encode())
