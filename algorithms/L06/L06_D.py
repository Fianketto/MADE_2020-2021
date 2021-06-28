import sys

s1 = (sys.stdin.buffer.readline().decode())
s2 = (sys.stdin.buffer.readline().decode())

n, m = len(s1) + 1, len(s2) + 1
dp = [[0 for j in range(m)] for i in range(n)]

for i in range(n):
    dp[i][0] = i
for j in range(m):
    dp[0][j] = j

for i in range(1, n):
    for j in range(1, m):
        if s1[i - 1] == s2[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
        else:
            dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

sys.stdout.buffer.write((str(dp[n - 1][m - 1]) + "\n").encode())
