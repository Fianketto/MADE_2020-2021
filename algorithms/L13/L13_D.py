import sys, threading
sys.setrecursionlimit(10 ** 9)
threading.stack_size(10 ** 8)


def solve():
    INF = float('inf')
    SNAIL_COUNT = 2


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

    def restore_path(path, from_vert, to_vert):
        path.append(str(from_vert + 1))
        if from_vert == to_vert:
            return
        for edge in rel[from_vert]:
            if edge.flow != edge.capacity or edge.capacity == 0:
                continue
            else:
                edge.flow = 0
                rel[edge.to_vert][edge.link].flow = 0
                restore_path(path, edge.to_vert, to_vert)
                break

    n, m, s, t = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
    s -= 1
    t -= 1
    rel = [[] for i in range(n)]

    for line in sys.stdin.buffer.read().decode().splitlines():
        u, v = tuple(map(int, line.split()))
        rel[u - 1].append(Edge(u - 1, v - 1, 1, len(rel[v - 1])))
        rel[v - 1].append(Edge(v - 1, u - 1, 0, len(rel[u - 1]) - 1))

    ans = 0
    path_found = False

    while not path_found:
        used = [False for i in range(n)]
        delta = push_flow(s, t, INF, used)
        if delta > 0:
            ans += delta
            if ans >= SNAIL_COUNT:
                path_found = True
        else:
            break

    if not path_found:
        sys.stdout.buffer.write("NO\n".encode())
    else:
        path1, path2 = [], []
        restore_path(path1, s, t)
        restore_path(path2, s, t)
        if len(path1) > len(path2):
            path1, path2 = path2, path1
        sys.stdout.buffer.write("YES\n".encode())
        sys.stdout.buffer.write((" ".join(path1) + "\n").encode())
        sys.stdout.buffer.write((" ".join(path2) + "\n").encode())


def main():
    solve()


if __name__ == "__main__":
    threading.Thread(target=main).start()
