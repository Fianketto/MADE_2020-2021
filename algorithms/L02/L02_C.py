"""
Цифровая сортировка строк, содержащих символы ['a' - 'z'].
"""

FIRST_LETTER_CODE = 97  # ASCII-код буквы 'a'
LETTER_COUNT = 26  # Всего символов в диапазоне ['a' - 'z']


def radix_sort(arr, step):
    global array
    cnt = [0 for i in range(LETTER_COUNT)]
    cnt_sum = [0 for i in range(LETTER_COUNT)]
    new_arr = ["" for i in range(n)]
    for s in arr:
        cnt[ord(s[step]) - FIRST_LETTER_CODE] += 1
    for i in range(1, LETTER_COUNT):
        cnt_sum[i] = cnt[i - 1] + cnt_sum[i - 1]
    for i in range(n):
        s = arr[i]
        order = cnt_sum[ord(s[step]) - FIRST_LETTER_CODE]
        new_arr[order] = s
        cnt_sum[ord(s[step]) - FIRST_LETTER_CODE] += 1
    array = new_arr


n, m, k = tuple(map(int, input().split()))
array = ["" for i in range(n)]

for i in range(n):
    array[i] = input().strip()

for step in range(k):
    radix_sort(array, m - 1 - step)

print("\n".join(array))
