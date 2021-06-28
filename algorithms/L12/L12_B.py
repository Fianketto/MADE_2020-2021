import sys


def get(x):
    if parent[x] != x:
        parent[x] = get(parent[x])
    return parent[x]


def join(x, y):
    x = get(x)
    y = get(y)
    if x == y:
        return
    if rank[x] > rank[y]:
        x, y = y, x
    if rank[x] == rank[y]:
        rank[y] += 1
    parent[x] = y
    kids[y].append(x)
    kids[y] += kids[x]


def add_exp(x, v):
    p = get(x)
    exp[p] += v
    for i in kids[p]:
        exp[i] += v


n, m = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
#n, m = tuple(map(int, input().split()))
rank = [0 for i in range(n)]
parent = [i for i in range(n)]
kids = [[] for i in range(n)]
exp = [0 for i in range(n)]
ans = []

for line in sys.stdin.buffer.read().decode().splitlines():
#for i in range(m):
    a = list(line.split())
    #a = list(input().split())
    if a[0] == "join":
        join(int(a[1]) - 1, int(a[2]) - 1)
    elif a[0] == "get":
        ans.append(str(exp[int(a[1]) - 1]))
    elif a[0] == "add":
        add_exp(int(a[1]) - 1, int(a[2]))

    #print(f"rank: {rank}, parent: {parent}, kids: {kids}, exp: {exp}, ans: {ans}")


sys.stdout.buffer.write("\n".join(ans).encode())
