import sys

n, k = list(map(int, sys.stdin.buffer.readline().decode().split()))
a = list(map(int, sys.stdin.buffer.readline().decode().split()))
a = [0] + a + [0]

coins_collected = [0] * (n + 2)
parent = [0] * (n + 2)
for i in range(1, n):
    max_element = coins_collected[i - 1]
    parent[i] = i - 1
    for j in range(max(0, i - k), i):
        if coins_collected[j] > max_element:
            max_element = coins_collected[j]
            parent[i] = j
    coins_collected[i] = a[i] + max_element

path = [n]
prev_cell_id = parent[n - 1]
while prev_cell_id > 0:
    path.append(prev_cell_id + 1)
    prev_cell_id = parent[prev_cell_id]
step_count = len(path)
path.append(1)
path.reverse()

sys.stdout.buffer.write((str(coins_collected[n - 1]) + "\n").encode())
sys.stdout.buffer.write((str(step_count) + "\n").encode())
sys.stdout.buffer.write((" ".join(map(str, path)) + "\n").encode())
