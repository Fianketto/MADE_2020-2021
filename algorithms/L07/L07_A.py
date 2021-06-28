import sys

print(-37%21)
CONST1 = 2 ** 16
CONST2 = 2 ** 30

n, x, y, a0 = list(map(int, sys.stdin.buffer.readline().decode().split()))
m, z, t, b0 = list(map(int, sys.stdin.buffer.readline().decode().split()))

a = [0 for i in range(n)]
b = [0 for i in range(2 * m)]
c = [0 for i in range(2 * m)]
a[0] = a0
b[0] = b0
c[0] = b0 % n
p_sum = [0 for i in range(n)]

for i in range(1, n):
    a[i] = (x * a[i - 1] + y) % CONST1
for j in range(1, 2 * m):
    b[j] = (z * b[j - 1] + t) % CONST2
    c[j] = b[j] % n

p_sum[0] = a[0]
for i in range(1, n):
    p_sum[i] = p_sum[i - 1] + a[i]

ans = 0
for j in range(m):
    left = min(c[2 * j], c[2 * j + 1])
    right = max(c[2 * j], c[2 * j + 1])
    if left == 0:
        ans += p_sum[right]
    else:
        ans += p_sum[right] - p_sum[left - 1]
sys.stdout.buffer.write((str(ans) + "\n").encode())
