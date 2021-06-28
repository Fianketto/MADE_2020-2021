import sys

INF = float('inf')
BIG_NUMBER = 100000

n = int(sys.stdin.buffer.readline().decode())
dist = [[] for i in range(n)]
i = 0
for line in sys.stdin.buffer.read().decode().splitlines():
    dist[i] = list(map(int, line.split()))
    for j in range(n):
        if dist[i][j] == BIG_NUMBER:
            dist[i][j] = INF
    i += 1


path = [[i for i in range(n)] for j in range(n)]

starting = -1
for k in range(n):
    for u in range(n):
        for v in range(n):
            if dist[u][k] < INF and dist[k][v] < INF and dist[u][k] + dist[k][v] < dist[u][v]:
                dist[u][v] = max(-INF, dist[u][k] + dist[k][v])
                path[u][v] = path[u][k]
    for u in range(n):
        if dist[u][u] < 0:
            starting = u
            break
    if starting >= 0:
        break

cycle_exists = starting >= 0
if not cycle_exists:
    sys.stdout.buffer.write("NO".encode())
else:
    u = starting
    ans = []
    ans_set = set()
    while u not in ans_set:
        ans.append(u + 1)
        ans_set.add(u)
        u = path[u][starting]

    sys.stdout.buffer.write(("YES\n" + str(len(ans)) + "\n").encode())
    sys.stdout.buffer.write((" ".join(map(str, ans))).encode())
