"""
k-ая порядковая статистика
"""
import random


def get_median(arr, i1, i2, i3):
    a1, a2, a3 = arr[i1], arr[i2], arr[i3]
    if min(a1, a2, a3) == a1:
        return min(a2, a3)
    elif min(a1, a2, a3) == a2:
        return min(a1, a3)
    return min(a1, a2)


def get_k_statistic(arr, left, right, k):
    temp_var = False
    if left < right:
        # pivot_id = random.randrange(left, right)  # id опорного элемента
        pivot_id = left
        pivot = arr[pivot_id]  # и сам опорный элемент
        arr[pivot_id], arr[right] = arr[right], arr[pivot_id]  # уводим опорный элемент в конец
        left_pointer, right_pointer = left, right - 1  # указатели слева и справа для сравнения элементов
        identical_left, identical_right = left - 1, right  # указатели слева и справа для элементов, равных опорному
        while left_pointer <= right_pointer:
            while arr[left_pointer] < pivot:
                left_pointer += 1
            while arr[right_pointer] > pivot:
                right_pointer -= 1
            if right_pointer <= left_pointer:
                break

            arr[left_pointer], arr[right_pointer] = arr[right_pointer], arr[left_pointer]
            if arr[left_pointer] == pivot:
                identical_left += 1
                arr[identical_left], arr[left_pointer] = arr[left_pointer], arr[identical_left]
            left_pointer += 1
            if arr[right_pointer] == pivot:
                identical_right -= 1
                arr[identical_right], arr[right_pointer] = arr[right_pointer], arr[identical_right]
            right_pointer -= 1

        arr[left_pointer], arr[right] = arr[right], arr[left_pointer]  # возвращаем опорный элемент с конца

        if left_pointer == k:
            return arr[left_pointer]
        if left_pointer > k:
            temp_var = True
        right_pointer = left_pointer - 1
        left_pointer += 1
        for p in range(left, identical_left + 1):  # собираем все одинаковые элементы слева
            arr[p], arr[right_pointer] = arr[right_pointer], arr[p]
            # right_pointer -= 1
        for p in range(right - 1, identical_right - 1, -1):  # то же самое справа
            arr[p], arr[left_pointer] = arr[left_pointer], arr[p]
            # left_pointer += 1

        if temp_var:
            return get_k_statistic(arr, left, right_pointer, k)
        else:
            return get_k_statistic(arr, left_pointer, right, k)
    elif left == right:
        return arr[left]


n = int(input())
a = list(map(int, input().split()))
m = int(input())
ans = [0 for i in range(m)]

for query_num in range(m):
    i, j, k2 = tuple(map(int, input().split()))
    b = a[i - 1: j]
    q = get_k_statistic(b, 0, len(b) - 1, k2 - 1)
    ans[query_num] = q
    # print(q)

print("\n".join(map(str, ans)))
