"""
Быстрая сортировка.
"""
import random


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


N = int(input())
a = list(map(int, input().split()))
quick_sort(a, 0, len(a) - 1)
print(" ".join(map(str, b)))
