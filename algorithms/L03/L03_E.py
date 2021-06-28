def enough_time(t):
    copy_cnt = 1 + (t - t1) // t1 + (t - t1) // t2
    if copy_cnt >= n:
        return 1
    return 0


ITER_COUNT = 100
n, x, y = list(map(int, input().split()))
t1, t2 = min(x, y), max(x, y)

left_b = 0
right_b = n * t2

for i in range(ITER_COUNT):
    x = (right_b + left_b) // 2
    if enough_time(x) == 1:
        right_b = x
    else:
        left_b = x
print(x + 1)
