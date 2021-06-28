import sys, threading
sys.setrecursionlimit(10 ** 9)
threading.stack_size(10 ** 8)

cycle_exists = False


def solve():
    def dfs(v):
        global cycle_exists
        color[v] = 1
        for u in rel[v]:
            if color[u] == 0:
                dfs(u)
            if color[u] == 1:
                cycle_exists = True
                return
        color[v] = 2

    def dfs_sort(v):
        used[v] = True
        for u in rel[v]:
            if not used[u]:
                dfs_sort(u)
        ans.append(v + 1)

    n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
    rel = [[] for i in range(n)]
    color = [0 for i in range(n)]
    used = [False for i in range(n)]
    ans = []

    for line in sys.stdin.buffer.read().decode().splitlines():
        u, v = tuple(map(int, line.split()))
        rel[u - 1].append(v - 1)

    for v in range(n):
        if color[v] == 0 and not cycle_exists:
            dfs(v)

    if cycle_exists:
        ans = [-1]
    else:
        for v in range(n):
            if not used[v]:
                dfs_sort(v)
        ans.reverse()

    sys.stdout.buffer.write(" ".join(tuple(map(str, ans))).encode())


def main():
    solve()


if __name__ == "__main__":
    threading.Thread(target=main).start()
