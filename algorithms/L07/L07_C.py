import sys


def initialize_array_t():
    for i in range(n):
        for j in range(f[i], i + 1):
            t[i] += a[j]


def set_element(i, x):
    index = i - 1
    dif = x - a[index]
    a[index] = x
    while index < n:
        t[index] += dif
        index = index | (index + 1)


def get_prefix_sum(i):
    res = 0
    index = i - 1
    while index >= 0:
        res += t[index]
        index = f[index] - 1
    return res


def rsq(left, right):
    if left == 1:
        return get_prefix_sum(right)
    return get_prefix_sum(right) - get_prefix_sum(left - 1)


n = int(sys.stdin.buffer.readline().decode())
a = list(map(int, sys.stdin.buffer.readline().decode().split()))

f = [i & i + 1 for i in range(n)]
t = [0 for i in range(n)]
initialize_array_t()

ans = []
for line in sys.stdin.buffer.read().decode().splitlines():
    op, i, x = list(line.split())
    if op == "set":
        set_element(int(i), int(x))
    else:
        ans.append(str(rsq(int(i), int(x))))

sys.stdout.buffer.write("\n".join(ans).encode())
