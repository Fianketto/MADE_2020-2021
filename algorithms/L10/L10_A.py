import sys, threading
sys.setrecursionlimit(10 ** 9)
threading.stack_size(10 ** 8)


def solve():
    def dfs(v, comp_number):
        component[v] = comp_number
        for u in rel[v]:
            if component[u] == 0:
                dfs(u, comp_number)

    n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
    rel = [[] for i in range(n)]
    component = [0 for i in range(n)]
    for line in sys.stdin.buffer.read().decode().splitlines():
        u, v = tuple(map(int, line.split()))
        rel[u - 1].append(v - 1)
        rel[v - 1].append(u - 1)

    cnt = 0
    for v in range(n):
        if component[v] == 0:
            cnt += 1
            dfs(v, cnt)

    component = tuple(map(str, component))
    sys.stdout.buffer.write((str(cnt) + "\n").encode())
    sys.stdout.buffer.write((" ".join(component) + "\n").encode())


def main():
    solve()


if __name__ == "__main__":
    threading.Thread(target=main).start()
