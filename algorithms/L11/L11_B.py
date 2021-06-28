import sys
import heapq


INF = float('inf')
n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))

min_dist = [INF for i in range(n)]
used = [False for i in range(n)]
edges = [[] for i in range(n)]

min_dist[0] = 0
used[0] = False
queue_of_vert = []
heapq.heappush(queue_of_vert, (0, 0))


class Edge:
    def __init__(self, to, weight):
        self.to = to
        self.weight = weight

    def __repr__(self):
        return "to:" + str(self.to) + ";_weight:" + str(self.weight)

    def __lt__(self, other):
        return self.weight < other.weight


for line in sys.stdin.buffer.read().decode().splitlines():
    x, y, w = tuple(map(int, line.split()))
    edges[x - 1].append(Edge(y - 1, w))
    edges[y - 1].append(Edge(x - 1, w))

while len(queue_of_vert) > 0:
    d, u = heapq.heappop(queue_of_vert)
    if d != min_dist[u]:
        continue
    if min_dist[u] == INF:
        break

    for edge in edges[u]:
        if min_dist[u] + edge.weight < min_dist[edge.to]:
            min_dist[edge.to] = min_dist[u] + edge.weight
            heapq.heappush(queue_of_vert, (min_dist[edge.to], edge.to))

sys.stdout.buffer.write((" ".join(map(str, min_dist))).encode())
