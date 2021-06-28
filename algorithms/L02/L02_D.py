"""
Гриша после дискотеки.
Поиск кол-ва подстрок, в которых каждый символ встречается не более соответствующего заданного числа
"""


def get_id(k):
    # порядковый номер (id) буквы на позиции k в строке Гриши (n)
    return ord(n[k]) - FIRST_LETTER_CODE


FIRST_LETTER_CODE = ord('a')  # ASCII-код буквы 'a'
LETTER_COUNT = 26  # Всего символов в диапазоне ['a' - 'z']

cnt_t = [0 for i in range(LETTER_COUNT)]    # кол-во каждого символа в строке t
cnt_current = [0 for i in range(LETTER_COUNT)]

first_line = input().strip()
n = input().strip()
t = input().strip()

for i in range(len(t)):
    cnt_t[ord(t[i]) - FIRST_LETTER_CODE] += 1

valid_substrings_cnt = int(len(n) * (len(n) + 1) / 2)   # максимально возможное число подстрок
left_pointer = 0
right_pointer = 0
enough_symbols = True
cnt_current[get_id(0)] += 1
for left_pointer in range(len(n)):
    if right_pointer == left_pointer - 1:
        cnt_current[get_id(left_pointer)] += 1
    right_pointer = max(right_pointer, left_pointer)
    cnt_now = cnt_current[get_id(right_pointer)]
    cnt_max = cnt_t[get_id(right_pointer)]
    enough_symbols = cnt_now <= cnt_max
    while enough_symbols and right_pointer < len(n) - 1:
        right_pointer += 1
        cnt_current[get_id(right_pointer)] += 1
        cnt_now = cnt_current[get_id(right_pointer)]
        cnt_max = cnt_t[get_id(right_pointer)]
        enough_symbols = cnt_now <= cnt_max
    if not enough_symbols:
        valid_substrings_cnt -= len(n) - right_pointer
        cnt_current[get_id(left_pointer)] -= 1

print(valid_substrings_cnt)
