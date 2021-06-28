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


def bfs():
    d = [-1 for i in range(n)]
    d[s] = 0
    queue = [s]

    while len(queue) > 0:
        v = queue.pop(0)
        for edge in rel[v]:
            u = edge.to_vert
            if edge.flow < edge.capacity and d[u] == -1:
                d[u] = d[v] + 1
                queue.append(u)
    return d[t] != -1


def change_belonging(belongs_to_s, v):
    if belongs_to_s[v]:
        return
    belongs_to_s[v] = True
    for edge in rel[v]:
        if edge.flow != edge.capacity:
            change_belonging(belongs_to_s, edge.to_vert)


def restore_parts():
    global total_capacity
    belongs_to_s = [False for j in range(n)]
    change_belonging(belongs_to_s, s)
    i = 0
    for edge in edge_order:
        u = edge.from_vert
        v = edge.to_vert
        i += 1
        if belongs_to_s[u] == belongs_to_s[v]:
            continue
        cut_edges.append(str(i))
        total_capacity += edge.capacity


n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))

rel = [[] for i in range(n)]
edge_order = []
cut_edges = []
total_capacity = 0
s, t = 0, n - 1

for line in sys.stdin.buffer.read().decode().splitlines():
    u, v, c = tuple(map(int, line.split()))
    rel[u - 1].append(Edge(u - 1, v - 1, c, len(rel[v - 1])))
    rel[v - 1].append(Edge(v - 1, u - 1, c, len(rel[u - 1]) - 1))
    edge_order.append(rel[u - 1][-1])


ans = 0
while bfs():
    used = [False for i in range(n)]
    path = [None for i in range(n)]
    delta = push_flow(s, t, INF, used)
    if delta > 0:
        ans += delta
    else:
        break

restore_parts()
sys.stdout.buffer.write((str(len(cut_edges)) + " " + str(total_capacity) + "\n").encode())
sys.stdout.buffer.write((" ".join(cut_edges) + "\n").encode())
