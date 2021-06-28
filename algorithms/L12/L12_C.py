import sys


class Vert:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def weight(u, v):
    return (u.x - v.x) ** 2 + (u.y - v.y) ** 2


INF = 10 ** 10
n = int(sys.stdin.buffer.readline().decode())
vertices = [None for i in range(n)]

i = 0
for line in sys.stdin.buffer.read().decode().splitlines():
    x, y = tuple(map(int, line.split()))
    vertices[i] = Vert(x, y)
    i += 1

dist = [INF for i in range(n)]
dist[0] = 0
used = [False for i in range(n)]
ans = 0
for i in range(n):
    min_dist = INF
    for j in range(n):
        if not used[j] and dist[j] < min_dist:
            min_dist = dist[j]
            u = j
    ans += min_dist ** 0.5
    used[u] = True
    for v in range(n):
        dist[v] = min(dist[v], weight(vertices[u], vertices[v]))

print(ans)
