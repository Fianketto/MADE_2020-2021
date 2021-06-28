from math import log, ceil
import heapq


def build_tree():
    for i in range(n - 1, -1, -1):
        if i > n // 2 - 1 + n_original:
            tree[i] = INF
        elif i > n // 2 - 1:
            tree[i] = arr[i - n // 2]
        else:
            tree[i] = min(tree[2 * i + 1], tree[2 * i + 2])


def get_min(a, b, left, right, v):
    if right < a or left > b:
        return INF
    elif right <= b and left >= a:
        return tree[v]
    else:
        mid = (left + right - 1) / 2
        left_min = get_min(a, b, left, mid, 2 * v + 1)
        right_min = get_min(a, b, mid + 1, right, 2 * v + 2)
        return min(left_min, right_min)


INF = 2 ** 31 - 1
#with open('rmq.in') as f:
f = open('rmq.in')
input_data = f.read().split("\n")
n_original, m = list(map(int, input_data[0].split()))

#n_original, m = list(map(int, input().split()))
log_n = ceil(log(n_original, 2))
n = 2 ** (log_n + 1) - 1
last_row = 2 ** log_n

arr = [0 for i in range(n_original)]
tree = ['' for i in range(n)]

queries = ['' for i in range(m)]
q_left = [[] for i in range(n_original)]
q_right = [[] for i in range(n_original)]
current_elements = []

for q_num in range(m):
    #i, j, q = list(map(int, input().split()))
    i, j, q = list(map(int, input_data[q_num + 1].split()))
    queries[q_num] = [i - 1, j - 1, q]
    q_left[i - 1].append(q)
    q_right[j - 1].append(q)
f.close()

for i in range(n_original):
    #print(f"now i = {i}")
    for q in q_left[i]:
        #current_elements.append(q)
        heapq.heappush(current_elements, -q)
        #print(f"\tnext element of q_left is {q}, cur_els: {current_elements}")
    if i > 0:
        #print(f"\ti is > 0 so deleting elements from q_right!")
        for q in q_right[i - 1]:
            current_elements.remove(-q)
            heapq.heapify(current_elements)

    if len(current_elements) > 0:
        #arr[i] = max(current_elements)
        arr[i] = -current_elements[0]

# tree[n // 2: n // 2 + n_original] = arr
build_tree()

consistent = True
for q_num in range(m):
    real_min = get_min(queries[q_num][0], queries[q_num][1], 0, last_row - 1, 0)
    if real_min != queries[q_num][2]:
        consistent = False
        break

if consistent:
    ans = "consistent\n" + " ".join(list(map(str, arr)))
else:
    ans = "inconsistent"

f_out = open("rmq.out", "w")
print(ans.strip(), file=f_out, end="")
#print(ans)
f_out.close()
