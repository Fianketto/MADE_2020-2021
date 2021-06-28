import sys


def lower_bound(x):
    left_b = -1
    right_b = n
    while left_b < right_b - 1:
        m = (left_b + right_b) // 2
        if x <= arr[m]:
            right_b = m
        else:
            left_b = m
    return right_b


n = int(sys.stdin.readline())
arr = list(map(int, sys.stdin.readline().split()))
k = int(sys.stdin.readline())
ans = [0 for i in range(k)]
arr.sort()

for i in range(k):
    lb, rb = tuple(map(int, sys.stdin.readline().split()))
    lb_id = lower_bound(lb)
    rb_id = lower_bound(rb + 1)
    ans[i] = rb_id - lb_id

sys.stdout.write(" ".join(map(str, ans)))
