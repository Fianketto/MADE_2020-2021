import sys, threading
sys.setrecursionlimit(10 ** 9)
threading.stack_size(10 ** 8)


def solve():
    def dfs(v, comp_number):
        component[v] = comp_number
        for u in rel2[v]:
            if component[u] == 0:
                dfs(u, comp_number)

    def dfs_sort(v):
        used[v] = True
        for u in rel1[v]:
            if not used[u]:
                dfs_sort(u)
        order.append(v)

    n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
    rel1 = [[] for i in range(n)]
    rel2 = [[] for i in range(n)]
    component = [0 for i in range(n)]
    used = [False for i in range(n)]
    cond_edges = [set() for i in range(n)]
    order = []

    for line in sys.stdin.buffer.read().decode().splitlines():
        u, v = tuple(map(int, line.split()))
        rel1[u - 1].append(v - 1)
        rel2[v - 1].append(u - 1)

    for v in range(n):
        if not used[v]:
            dfs_sort(v)
    order.reverse()

    cnt = 0
    for v in order:
        if component[v] == 0:
            cnt += 1
            dfs(v, cnt)

    for v in range(n):
        for u in rel1[v]:
            if component[u] != component[v]:
                cond_edges[component[u] - 1].add(component[v] - 1)

    ans = 0
    for i in range(n):
        ans += len(cond_edges[i])

    sys.stdout.buffer.write(str(ans).encode())


def main():
    solve()


if __name__ == "__main__":
    threading.Thread(target=main).start()
