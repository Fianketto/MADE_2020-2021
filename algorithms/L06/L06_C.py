import sys

n = int(sys.stdin.buffer.readline().decode())
a = list(map(int, sys.stdin.buffer.readline().decode().split()))

dp = [1] * n
parent = [-1] * n

for i in range(1, n):
    prev_max = 0
    for j in range(i):
        if dp[j] > prev_max and a[j] < a[i]:
            prev_max = dp[j]
            parent[i] = j
    dp[i] = prev_max + 1

max_length = 0
needed_id = 0
for i in range(n):
    if dp[i] > max_length:
        max_length = dp[i]
        needed_id = i

ans = []
while needed_id >= 0:
    ans.append(str(a[needed_id]))
    needed_id = parent[needed_id]

ans.reverse()
sys.stdout.buffer.write((str(max_length) + "\n").encode())
sys.stdout.buffer.write((" ".join(ans) + "\n").encode())
