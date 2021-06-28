"""
Сортировка пузырьком.
Переменная array_changed служит для отслеживания изменения массива на текущей итерации.
Если массив не изменился, значит он уже отсортирован => досрочно выходим из цикла.
"""

N = int(input())
a = list(map(int, input().split()))
for k in range(N - 1):
    array_changed = False
    for i in range(N - 1 - k):
        if a[i] > a[i + 1]:
            a[i], a[i + 1] = a[i + 1], a[i]
            array_changed = True
    if not array_changed:
        break
print(" ".join(map(str, a)))
