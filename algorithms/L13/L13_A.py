import sys


INF = float('inf')


class Edge:
    def __init__(self, from_vert, to_vert, capacity, link):
        self.from_vert = from_vert
        self.to_vert = to_vert
        self.capacity = capacity
        self.link = link
        self.flow = 0

    def __repr__(self):
        repr = f"|{self.from_vert}->{self.to_vert}: {self.flow}/{self.capacity}| "
        return repr


def push_flow(v, t, cur_flow, used):
    used[v] = True
    if v == t:
        return cur_flow
    for edge in rel[v]:
        u = edge.to_vert
        if not used[u] and edge.flow < edge.capacity:
            next_flow = min(cur_flow, edge.capacity - edge.flow)
            delta = push_flow(u, t, next_flow, used)
            if delta > 0:
                edge.flow += delta
                back_edge = rel[u][edge.link]
                back_edge.flow -= delta
                return delta
    return 0


n = int(sys.stdin.buffer.readline().decode())
m = int(sys.stdin.buffer.readline().decode())
rel = [[] for i in range(n)]
s, t = 0, n - 1

for line in sys.stdin.buffer.read().decode().splitlines():
    u, v, c = tuple(map(int, line.split()))
    rel[u - 1].append(Edge(u - 1, v - 1, c, len(rel[v - 1])))
    rel[v - 1].append(Edge(v - 1, u - 1, c, len(rel[u - 1]) - 1))


ans = 0
'''
for i in range(n):
    for e in rel[i]:
        print(i, e)
'''

while True:
    used = [False for i in range(n)]
    delta = push_flow(s, t, INF, used)
    if delta > 0:
        ans += delta
    else:
        break

print(ans)
