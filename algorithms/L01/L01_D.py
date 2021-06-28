"""
Подсчет количества инверсий в масиве с помощью сортировки слиянием.
Код - тот же самый, что и в задаче C (сортировка слиянием).
Отличие - новая переменная inversion_count.
"""
inversion_count = 0


def merge(arr1, arr2):
    global inversion_count
    arr1_len = len(arr1)
    arr2_len = len(arr2)
    arr3_len = arr1_len + arr2_len
    arr3 = [0 for i in range(arr3_len)]
    i, j = 0, 0
    while i + j < arr3_len:
        if j == arr2_len or (i < arr1_len and arr1[i] < arr2[j]):
            arr3[i + j] = arr1[i]
            i += 1
        else:
            arr3[i + j] = arr2[j]
            j += 1
            inversion_count += arr1_len - i  # вот тут считаем кол-во инверсий
    return arr3


def merge_sort(arr):
    if len(arr) == 1:
        return arr
    arr1 = merge_sort(arr[:len(arr) // 2])
    arr2 = merge_sort(arr[len(arr) // 2:])
    return merge(arr1, arr2)


N = int(input())
a = list(map(int, input().split()))
sorted_array = merge_sort(a)
# print(" ".join(map(str, sorted_array)))
print(inversion_count)
