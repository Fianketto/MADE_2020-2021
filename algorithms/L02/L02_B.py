"""
Сортировка подсчетом
"""

N = 100
arr = list(map(int, input().split()))
cnt = [0 for i in range(N + 1)]

for i in arr:
    cnt[i] += 1

ind = 0
for i in range(N + 1):
    for j in range(cnt[i]):
        arr[ind] = i
        ind += 1

print(" ".join(map(str, arr)))
