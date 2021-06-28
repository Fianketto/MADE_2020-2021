from math import log, ceil
import sys


def build_tree():
    for i in range(n - 1, -1, -1):
        if i > n // 2 - 1 + n_original:
            tree[i] = INF
        elif i > n // 2 - 1:
            #tree[i] = arr[i - n // 2]
            continue
        else:
            tree[i] = min(tree[2 * i + 1], tree[2 * i + 2])


def get_min(a, b, left, right, v):
    print(f"called min on [{a}, {b}], vert id = {v}, resp for [{left}, {right}]", end="\t")
    if right < a or left > b:
        print(f"out of [{a}, {b}], returning INF")
        return INF
    elif right <= b and left >= a:
        print(f"inside [{a}, {b}], returning tree[{v}] = {tree[v]}")
        return get_real_value(v)
    else:
        if mark[v] != [1, 0]:
            push_mark_downwards(v)
        m = (left + right - 1) / 2
        print(f"overlap, returning min for vertices resp for [{left}, {m}] and [{m + 1}, {right}]")
        left_min = get_min(a, b, left, m, 2 * v + 1)
        right_min = get_min(a, b, m + 1, right, 2 * v + 2)
        return min(left_min, right_min)


def add_value(a, b, left, right, v, x):
    print(f"called ADD {x} on [{a}, {b}], vert id = {v}, resp for [{left}, {right}]", end="\t")
    if right < a or left > b:
        print(f"out of [{a}, {b}], just returning")
        return
    elif right <= b and left >= a:
        print(f"inside [{a}, {b}]")
        print(f"going to call stack with mark [1, {x}] for {v}")
        stack_marks([1, x], v)
        update_min_upwards(v)
    else:
        print(f"overlap, now checking if needed to push")
        if mark[v] != [1, 0]:
            print(f"going to push mark from {v}")
            push_mark_downwards(v)
        m = (left + right - 1) / 2
        print(f"PART 1: will now ADD {x} for vert {2*v+1} resp for [{left}, {m}]")
        add_value(a, b, left, m, 2 * v + 1, x)
        print(f"PART 2: will now ADD {x} for vert {2*v+2} resp for [{m+1}, {right}]")
        add_value(a, b, m + 1, right, 2 * v + 2, x)


def set_value(a, b, left, right, v, x):
    if right < a or left > b:
        return
    elif right <= b and left >= a:
        print(f"going to call stack with mark [0, {x}] for {v}")
        stack_marks([0, x], v)
        update_min_upwards(v)
    else:
        if mark[v] != [1, 0]:
            push_mark_downwards(v)
        m = (left + right - 1) / 2
        set_value(a, b, left, m, 2 * v + 1, x)
        set_value(a, b, m + 1, right, 2 * v + 2, x)


def stack_marks(new_mark, v):
    print(f"called stack with {new_mark} for {v}, current mark for {v} is {mark[v]}")
    m1 = new_mark[0] * mark[v][0]
    m2 = new_mark[0] * mark[v][1] + new_mark[1]
    print(f"returning mark [{m1}, {m2}] for {v}")
    mark[v] = [m1, m2]


def update_min_upwards(v):
    while v > 0:
        parent_v = (v - 1) // 2
        sister_v = v + 2 * (v % 2) - 1
        tree[parent_v] = min(get_real_value(v), get_real_value(sister_v))
        v = parent_v


def get_real_value(v):
    return tree[v] * mark[v][0] + mark[v][1]


def push_mark_downwards(v):
    print("PUSH!", end=" ")
    if v <= n // 2 - 1:  # если не лист
        print(f"not a leave, going to stack {mark[v]} of {v} onto childs {2*v+1} and {2*v+2}")
        stack_marks(mark[v], 2 * v + 1)
        stack_marks(mark[v], 2 * v + 2)
    print("ENDED PUSHING!")
    tree[v] = get_real_value(v)
    mark[v] = [1, 0]
    print(f"now tree[{v}] = {tree[v]} and mark[{v}] = {mark[v]}")


INF = float('inf')

n_original = int(sys.stdin.buffer.readline().decode())
#arr = list(map(int, sys.stdin.buffer.readline().decode().split()))

log_n = ceil(log(n_original, 2))
n = 2 ** (log_n + 1) - 1
last_row = 2 ** log_n

mark = [[1, 0] for i in range(n)]
tree = ['' for i in range(n)]
tree[n // 2 : n // 2 + n_original] = list(map(int, sys.stdin.buffer.readline().decode().split()))

build_tree()

#print(arr)
#print(mark)
#print(tree)

ans = []
for i in range(99):
    inp = list(input().split())
    if inp[0] == "min":
        ans.append(str(get_min(int(inp[1]) - 1, int(inp[2]) - 1, 0, last_row - 1, 0)))
        print(get_min(int(inp[1]) - 1, int(inp[2]) - 1, 0, last_row - 1, 0))
    elif inp[0] == "set":
        set_value(int(inp[1]) - 1, int(inp[2]) - 1, 0, last_row - 1, 0, int(inp[3]))
    else:
        add_value(int(inp[1]) - 1, int(inp[2]) - 1, 0, last_row - 1, 0, int(inp[3]))

    print(tree)
    print(mark)

sys.stdout.buffer.write("\n".join(ans).encode())
