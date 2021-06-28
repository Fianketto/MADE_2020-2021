"""
k-ая порядковая статистика
"""
import random
import sys


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


def quick_sort(arr, left, right):
    if left < right:
        pivot_id = random.randrange(left, right)  # id опорного элемента
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
        right_pointer = left_pointer - 1
        left_pointer += 1
        for k in range(left, identical_left + 1):  # собираем все одинаковые элементы слева
            arr[k], arr[right_pointer] = arr[right_pointer], arr[k]
            right_pointer -= 1
        for k in range(right - 1, identical_right - 1, -1):  # то же самое справа
            arr[k], arr[left_pointer] = arr[left_pointer], arr[k]
            left_pointer += 1
        quick_sort(arr, left, right_pointer)
        quick_sort(arr, left_pointer, right)


# n = int(input())
# a = list(map(int, input().split()))
# m = int(input())
n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))
m = int(sys.stdin.readline())
d = {}
d2 = {}

for query_num in range(m):
    i, j, k2 = tuple(map(int, sys.stdin.readline().split()))
    unique_code = i * 1000 + j
    if unique_code in d.keys():
        if unique_code in d2.keys():
            q = d2[unique_code][k2 - 1]
        else:
            b = a[i - 1: j]
            quick_sort(b, 0, len(b) - 1)
            q = b[k2 - 1]
            d2[unique_code] = b.copy()
    else:
        b = a[i - 1: j]
        q = get_k_statistic(b, 0, len(b) - 1, k2 - 1)
        d[unique_code] = 1
    sys.stdout.write(str(q) + "\n")


"""
10
1 2 3 4 5 6 7 7 7 10
2
1 10 9
1 10 9

5
1 1 1
1 2 2
1 3 3
1 10 9
1 10 10
"""