from math import log, ceil
import sys


def build_tree():
    for i in range(n - 1, -1, -1):
        if i > n // 2 - 1 + n_original:
            tree[i] = INF
        elif i > n // 2 - 1:
            continue
        else:
            tree[i] = min(tree[2 * i + 1], tree[2 * i + 2])


def get_min(a, b, left, right, v):
    if right < a or left > b:
        return INF
    elif right <= b and left >= a:
        return get_real_value(v)
    else:
        if mark[v] is not None:
            push_mark_downwards(v)
        m = (left + right - 1) / 2
        left_min = get_min(a, b, left, m, 2 * v + 1)
        right_min = get_min(a, b, m + 1, right, 2 * v + 2)
        return min(left_min, right_min)


def add_value(a, b, left, right, v, x):
    if right < a or left > b:
        return
    elif right <= b and left >= a:
        stack_marks((1, x), v)
        update_min_upwards(v)
    else:
        if mark[v] is not None:
            push_mark_downwards(v)
        m = (left + right - 1) / 2
        add_value(a, b, left, m, 2 * v + 1, x)
        add_value(a, b, m + 1, right, 2 * v + 2, x)


def set_value(a, b, left, right, v, x):
    if right < a or left > b:
        return
    elif right <= b and left >= a:
        stack_marks((0, x), v)
        update_min_upwards(v)
    else:
        if mark[v] is not None:
            push_mark_downwards(v)
        m = (left + right - 1) / 2
        set_value(a, b, left, m, 2 * v + 1, x)
        set_value(a, b, m + 1, right, 2 * v + 2, x)


def stack_marks(new_mark, v):
    if mark[v] is None:
        mark[v] = (new_mark[0], new_mark[1])
    else:
        m1 = new_mark[0] * mark[v][0]
        m2 = new_mark[0] * mark[v][1] + new_mark[1]
        mark[v] = (m1, m2)


def update_min_upwards(v):
    while v > 0:
        parent_v = (v - 1) // 2
        sister_v = v + 2 * (v % 2) - 1
        tree[parent_v] = min(get_real_value(v), get_real_value(sister_v))
        v = parent_v


def get_real_value(v):
    if mark[v] is None:
        return tree[v]
    else:
        return tree[v] * mark[v][0] + mark[v][1]


def is_a_leave(v):
    return v > n // 2 - 1


def push_mark_downwards(v):
    if not is_a_leave(v):  # если не лист
        stack_marks(mark[v], 2 * v + 1)
        stack_marks(mark[v], 2 * v + 2)
    tree[v] = get_real_value(v)
    mark[v] = None


INF = float('inf')
n_original = int(sys.stdin.buffer.readline().decode())
log_n = ceil(log(n_original, 2))
n = 2 ** (log_n + 1) - 1
last_row = 2 ** log_n

mark = [None for i in range(n)]
tree = ['' for i in range(n)]
tree[n // 2: n // 2 + n_original] = list(map(int, sys.stdin.buffer.readline().decode().split()))

build_tree()
ans = []
for line in sys.stdin.buffer.read().decode().splitlines():
    inp = list(line.split())
    if inp[0] == "min":
        ans.append(str(get_min(int(inp[1]) - 1, int(inp[2]) - 1, 0, last_row - 1, 0)))
    elif inp[0] == "set":
        set_value(int(inp[1]) - 1, int(inp[2]) - 1, 0, last_row - 1, 0, int(inp[3]))
    else:
        add_value(int(inp[1]) - 1, int(inp[2]) - 1, 0, last_row - 1, 0, int(inp[3]))

sys.stdout.buffer.write("\n".join(ans).encode())
