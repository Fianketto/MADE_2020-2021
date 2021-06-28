import sys


def enough_rope(x):
    rope_cnt = 0
    if x == 0:
        return 1
    for i in range(n):
        rope_cnt += arr[i] // x
    if rope_cnt >= k:
        return 1
    return 0


ITER_COUNT = 100
n, k = list(map(int, sys.stdin.readline().split()))
arr = [0 for i in range(n)]
for i in range(n):
    arr[i] = int(sys.stdin.readline())

left_b = 0
right_b = max(arr) + 1

for i in range(ITER_COUNT):
    x = (right_b + left_b) // 2
    if enough_rope(x) == 1:
        left_b = x
    else:
        right_b = (x)

print(x)
