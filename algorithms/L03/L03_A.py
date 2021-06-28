n, k = tuple(map(int, input().split()))
arr = list(map(int, input().split()))
query = list(map(int, input().split()))


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


for i in range(k):
    x = query[i]
    if x <= arr[0]:
        ans = arr[0]
    elif x >= arr[n - 1]:
        ans = arr[n - 1]
    else:
        lb, ub = lower_bound(x), lower_bound(x + 1)
        if ub > lb:
            ans = arr[lb]
        elif abs(arr[lb - 1] - x) > abs(arr[ub] - x):
            ans = arr[ub]
        else:
            ans = arr[lb - 1]
    print(ans)
