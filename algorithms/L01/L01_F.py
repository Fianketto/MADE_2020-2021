"""
Сортировка королей по имени и порядковому числу
"""


def roman_to_arabic(roman_string):
    if len(roman_string) == 0:
        return 0
    arabic_value = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    current_part = arabic_value[roman_string[0]]
    total_sum = 0
    for i in range(1, len(roman_string)):
        if arabic_value[roman_string[i]] == arabic_value[roman_string[i - 1]]:
            current_part += arabic_value[roman_string[i]]
        elif arabic_value[roman_string[i]] > arabic_value[roman_string[i - 1]]:
            total_sum += arabic_value[roman_string[i]] - current_part
            current_part = 0
        else:
            total_sum += current_part
            current_part = arabic_value[roman_string[i]]
    total_sum += current_part
    return total_sum


n = int(input())
kings = [[] for i in range(n)]
for i in range(n):
    kings[i] = input().split()

sorted_kings = sorted(kings, key=lambda king: roman_to_arabic(king[1]))
kings = sorted(sorted_kings, key=lambda king: king[0])
for i in range(n):
    print(" ".join(map(str, kings[i])))
