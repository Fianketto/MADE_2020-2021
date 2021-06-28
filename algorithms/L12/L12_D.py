import sys


class Edge:
    def __init__(self, from_vert, to_vert, weight):
        self.from_vert = from_vert
        self.to_vert = to_vert
        self.weight = weight


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


n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
edges = [None for i in range(m)]
rank = [0 for i in range(n)]
parent = [i for i in range(n)]

i = 0
for line in sys.stdin.buffer.read().decode().splitlines():
    x, y, w = tuple(map(int, line.split()))
    edges[i] = Edge(int(x) - 1, int(y) - 1, int(w))
    i += 1

edges.sort(key=lambda e: e.weight)
ans = 0

for edge in edges:
    if get(edge.from_vert) != get(edge.to_vert):
        ans += edge.weight
        join(edge.from_vert, edge.to_vert)

print(str(ans))
