import sys

n, m = list(map(int, sys.stdin.buffer.readline().decode().split()))
a = []
for i in range(n):
    row = list(map(int, sys.stdin.buffer.readline().decode().split()))
    a.append(row)

coins_collected = [[0 for j in range(m)] for i in range(n)]
parent = [[-1 for j in range(m)] for i in range(n)]
direction_dict = {0: 'D', 1: 'R'}

coins_collected[0][0] = a[0][0]
for i in range(1, n):
    coins_collected[i][0] = coins_collected[i - 1][0] + a[i][0]
    parent[i][0] = 0
for j in range(1, m):
    coins_collected[0][j] = coins_collected[0][j - 1] + a[0][j]
    parent[0][j] = 1

for i in range(1, n):
    for j in range(1, m):
        if coins_collected[i][j - 1] >= coins_collected[i - 1][j]:
            coins_collected[i][j] = a[i][j] + coins_collected[i][j - 1]
            parent[i][j] = 1
        else:
            coins_collected[i][j] = a[i][j] + coins_collected[i - 1][j]
            parent[i][j] = 0

i, j = n - 1, m - 1
path = []

while i + j > 0:
    path.append(direction_dict[parent[i][j]])
    i, j = i - (1 - parent[i][j]), j - parent[i][j]
path.reverse()

sys.stdout.buffer.write((str(coins_collected[n - 1][m - 1]) + "\n").encode())
sys.stdout.buffer.write(("".join(path) + "\n").encode())

'''
1 5
1 -5 -4 3 5
'''

'''
for i in range(1, n):
    coins_collected[i][0] = coins_collected[i - 1][0] + a[i][0]
'''
