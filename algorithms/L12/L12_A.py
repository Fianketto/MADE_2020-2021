import sys


class Info:
    def __init__(self, min_element, max_element, cnt_element):
        self.min = min_element
        self.max = max_element
        self.cnt = cnt_element

    def get_attributes(self):
        return " ".join([str(self.min + 1), str(self.max + 1), str(self.cnt)])


def get(x):
    if parent[x] != x:
        parent[x] = get(parent[x])
    return parent[x]


def join(x, y):
    x = get(x)
    y = get(y)
    if x == y:
        return
    if rank[x] > rank[y]:
        x, y = y, x
    if rank[x] == rank[y]:
        rank[y] += 1
    parent[x] = y
    info[y].max = max(info[y].max, info[x].max)
    info[y].min = min(info[y].min, info[x].min)
    info[y].cnt += info[x].cnt


n = int(sys.stdin.buffer.readline().decode())
rank = [0 for i in range(n)]
parent = [i for i in range(n)]
info = [Info(i, i, 1) for i in range(n)]
ans = []

for line in sys.stdin.buffer.read().decode().splitlines():
    a = list(line.split())
    if a[0] == "union":
        join(int(a[1]) - 1, int(a[2]) - 1)
    elif a[0] == "get":
        p = get(int(a[1]) - 1)
        ans.append(info[p].get_attributes())

sys.stdout.buffer.write("\n".join(ans).encode())
