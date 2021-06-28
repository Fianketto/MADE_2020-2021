import sys
import math

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


def push_flow(v, t, cur_flow, used, min_delta):
    used[v] = True
    if v == t:
        return cur_flow
    for edge in rel[v]:
        u = edge.to_vert
        if not used[u] and edge.flow <= edge.capacity - min_delta:
            next_flow = min(cur_flow, edge.capacity - edge.flow)
            delta = push_flow(u, t, next_flow, used, min_delta)
            if delta > 0:
                edge.flow += delta
                back_edge = rel[u][edge.link]
                back_edge.flow -= delta
                return delta
    return 0


def bfs(min_delta):
    d = [-1 for i in range(n)]
    d[s] = 0
    queue = [s]

    while len(queue) > 0:
        v = queue.pop(0)
        for edge in rel[v]:
            u = edge.to_vert
            if edge.flow <= edge.capacity - min_delta and d[u] == -1:
                d[u] = d[v] + 1
                queue.append(u)
    return d[t] != -1


n = int(sys.stdin.buffer.readline().decode())
m = int(sys.stdin.buffer.readline().decode())
rel = [[] for i in range(n)]
edge_order = []
capacities = []
s, t = 0, n - 1

for line in sys.stdin.buffer.read().decode().splitlines():
    u, v, c = tuple(map(int, line.split()))
    rel[u - 1].append(Edge(u - 1, v - 1, c, len(rel[v - 1])))
    rel[v - 1].append(Edge(v - 1, u - 1, c, len(rel[u - 1]) - 1))
    edge_order.append(rel[u - 1][-1])
    capacities.append(c)
max_capacity = max(capacities)


ans = 0
for k in range(int(math.log2(max_capacity)), -1, -1):
    while bfs(2 ** k):
        used = [False for i in range(n)]
        path = [None for i in range(n)]
        delta = push_flow(s, t, INF, used, 2 ** k)
        if delta > 0:
            ans += delta
        else:
            break

flows = [0 for i in range(m)]
for i in range(len(edge_order)):
    flows[i] = str(edge_order[i].flow)

sys.stdout.buffer.write((str(ans) + "\n").encode())
sys.stdout.buffer.write(("\n".join(flows) + "\n").encode())
