import sys

THRESHOLD = 100
n = int(sys.stdin.buffer.readline().decode())
a = [0 for i in range(n)]
for i in range(n):
    a[i] = int(sys.stdin.buffer.readline().decode())

n += 1
m = n + 1
dp = [[0 for j in range(m)] for i in range(n)]
coupon_collected = [[0 for j in range(m)] for i in range(n)]
parent = [[0 for j in range(m)] for i in range(n)]

for i in range(n - 1):
    for j in range(i + 1, m):
        dp[i][j] = float('inf')

for i in range(1, n):
    for j in range(m - 1):
        if a[i - 1] <= THRESHOLD:
            if dp[i - 1][j] + a[i - 1] < dp[i - 1][j + 1]:
                dp[i][j] = dp[i - 1][j] + a[i - 1]
                coupon_collected[i][j] = coupon_collected[i - 1][j]
                parent[i][j] = 0
            else:
                dp[i][j] = dp[i - 1][j + 1]
                coupon_collected[i][j] = coupon_collected[i - 1][j + 1]
                parent[i][j] = 1
        else:
            prev_value = float('inf') if j == 0 else dp[i - 1][j - 1]
            prev_coupon_cnt = coupon_collected[i - 1][j + 1] if j == 0 else coupon_collected[i - 1][j - 1]
            if prev_value + a[i - 1] < dp[i - 1][j + 1]:
                dp[i][j] = prev_value + a[i - 1]
                coupon_collected[i][j] = prev_coupon_cnt + 1
                parent[i][j] = -1
            else:
                dp[i][j] = dp[i - 1][j + 1]
                coupon_collected[i][j] = coupon_collected[i - 1][j + 1]
                parent[i][j] = 1

min_payment = dp[n - 1][0]
coupon_cnt = coupon_collected[n - 1][0]
coupon_left = 0
days = []
for j in range(1, m - 1):
    if dp[n - 1][j] <= min_payment:
        min_payment = dp[n - 1][j]
        coupon_cnt = coupon_collected[n - 1][j]
        coupon_left = j
coupon_used = coupon_cnt - coupon_left

j = coupon_left
i = n - 1
while i > 0:
    if parent[i][j] == 1:
        days.append(str(i))
    j += parent[i][j]
    i -= 1
days.reverse()

sys.stdout.buffer.write((str(min_payment) + "\n").encode())
sys.stdout.buffer.write((str(coupon_left) + " " + str(coupon_used) + "\n").encode())
sys.stdout.buffer.write(("\n".join(days)).encode())
