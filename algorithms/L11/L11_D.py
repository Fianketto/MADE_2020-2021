import sys


INF = float('inf')


def dfs(u):
    used[u] = True
    exists[u] = False
    for v, w in rel[u]:
        if not used[v]:
            dfs(v)


class Edge:
    def __init__(self, from_edge, to_edge, weight):
        self.from_edge = from_edge
        self.to_edge = to_edge
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight


n, m, s = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
rel = [[] for i in range(n)]
edges = []
exists = [True for i in range(n)]
used = [False for i in range(n)]

for line in sys.stdin.buffer.read().decode().splitlines():
    u, v, weight = tuple(map(int, line.split()))
    rel[u - 1].append((v - 1, weight))
    edges.append(Edge(u - 1, v - 1, weight))


s -= 1
p = [-1 for i in range(n)]
dist = [INF for i in range(n)]
dist[s] = 0

for k in range(n):
    for edge in edges:
        u, v, weight = edge.from_edge, edge.to_edge, edge.weight
        if dist[u] + weight < dist[v]:
            dist[v] = dist[u] + weight
            p[v] = u


for edge in edges:
    u, v, weight = edge.from_edge, edge.to_edge, edge.weight
    if dist[v] > dist[u] + weight:
        dfs(v)

i = 0
ans = []
for distance in dist:
    if distance == INF:
        ans.append("*")
    elif not exists[i]:
        ans.append("-")
    else:
        ans.append(str(distance))
    i += 1

sys.stdout.buffer.write(("\n".join(ans)).encode())
