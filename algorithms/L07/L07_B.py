from math import log
import sys

C1 = 23
C2 = 21563
C3 = 16714589

A1 = 17
A2 = 751
A3 = 2

B1 = 13
B2 = 593
B3 = 5

n, m, a0 = list(map(int, sys.stdin.buffer.readline().decode().split()))
u, v = list(map(int, sys.stdin.buffer.readline().decode().split()))
log_n = int(log(n, 2)) + 2

a = [0 for i in range(n)]
a[0] = a0
for i in range(1, n):
    a[i] = (C1 * a[i - 1] + C2) % C3

dp = [[0 for j in range(log_n)] for i in range(n)]
for k in range(log_n):
    for i in range(n):
        if k == 0:
            dp[i][k] = a[i]
        else:
            ind = min(i + 2 ** (k - 1), n - 1)
            dp[i][k] = min(dp[i][k - 1], dp[ind][k - 1])

max_pow = [0 for i in range(n + 2)]
for i in range(2, n + 2):
    max_pow[i] = max_pow[i - 1]
    if 1 << max_pow[i] < i:
        max_pow[i] += 1
for i in range(n + 2):
    max_pow[i] -= 1


def get_min(u, v):
    left = min(u, v) - 1
    right = max(u, v) - 1
    k = max_pow[right - left + 2]
    ans = min(dp[left][k], dp[right - 2 ** k + 1][k])
    return ans


r = get_min(u, v)
for q in range(1, m):
    u = ((A1 * u + A2 + r + A3 * q) % n) + 1
    v = ((B1 * v + B2 + r + B3 * q) % n) + 1
    r = get_min(u, v)

sys.stdout.buffer.write((str(u) + " " + str(v) + " " + str(r) + "\n").encode())

# r - l + 1 = 1 -> min!
# r - l + 1 > 1
# k = max_pow[r - l + 2]
