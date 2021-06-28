import sys


class Map:
    def __init__(self):
        self.M = 10 ** 6
        self.A = 3691
        self.P = 2000003
        self.arr = ['' for i in range(self.M)]

    def hash_func(self, k):
        return ((k * self.A) % self.P) % self.M

    def put(self, k):
        h = self.hash_func(k)
        while not self.is_free_for_put(h):
            if self.arr[h] == k:
                return  # k уже есть
            h = self.hash_func(h + 1)
        self.arr[h] = k

    def exists(self, k):
        h = self.hash_func(k)
        while not self.is_empty(h):
            if self.arr[h] == k:
                return "true"
            else:
                h = self.hash_func(h + 1)
        return "false"

    def delete(self, k):
        h = self.hash_func(k)
        while not self.is_empty(h):
            if self.arr[h] == k:
                self.arr[h] = 'r'
                break
            else:
                h = self.hash_func(h + 1)

    def is_free_for_put(self, x):
        if self.arr[x] == '' or self.arr[x] == 'r':
            return True
        return False

    def is_empty(self, x):
        if self.arr[x] == '':
            return True
        return False


m = Map()
ans = []
for line in sys.stdin.buffer.read().decode().splitlines():
    a = list(line.split())
    if a[0][0] == "i":
        m.put(int(a[1]))
    elif a[0][0] == 'd':
        m.delete(int(a[1]))
    else:
        ans.append(m.exists(int(a[1])))

sys.stdout.buffer.write("\n".join(ans).encode())
