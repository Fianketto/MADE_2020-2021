import sys, threading
sys.setrecursionlimit(10 ** 9)
threading.stack_size(10 ** 8)

t = 0


def solve():
    def dfs(v, p):
        global t
        t += 1
        up[v] = t
        tin[v] = t
        used[v] = True
        count = 0
        for u in rel[v]:
            if u == p:
                continue
            if used[u]:
                up[v] = min(up[v], tin[u])
            else:
                dfs(u, v)
                count += 1
                up[v] = min(up[v], up[u])
                if p != -1 and up[u] >= tin[v]:
                    cut_points.add(v + 1)
        if p == -1 and count >= 2:
            cut_points.add(v + 1)

    n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
    rel = [[] for i in range(n)]
    used = [False for i in range(n)]
    tin = [0 for i in range(n)]
    up = [0 for i in range(n)]
    cut_points = set()

    for line in sys.stdin.buffer.read().decode().splitlines():
        u, v = tuple(map(int, line.split()))
        rel[u - 1].append(v - 1)
        rel[v - 1].append(u - 1)

    for v in range(n):
        if not used[v]:
            dfs(v, -1)

    cut_points_sorted = sorted(list(cut_points))

    sys.stdout.buffer.write((str(len(cut_points)) + "\n").encode())
    sys.stdout.buffer.write((" ".join(map(str, cut_points_sorted))).encode())


def main():
    solve()


if __name__ == "__main__":
    threading.Thread(target=main).start()
