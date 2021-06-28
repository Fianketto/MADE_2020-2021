from fractions import Fraction as frac


def pascal(N):
    all_pascal_lines.append([1])
    all_pascal_lines.append([1, 1])
    for n in range(2, N):
        new_row = []
        for k in range(n + 1):
            if k == 0 or k == n:
                new_el = 1
            else:
                new_el = all_pascal_lines[n - 1][k - 1] + all_pascal_lines[n - 1][k]
            new_row.append(new_el)
        all_pascal_lines.append(new_row)


set_count = int(input())
ans = [[] for i in range(set_count)]

for set_n in range(set_count):
    galton_list = []
    h = int(input())
    all_pascal_lines = []
    pascal(h)
    for i in range(h):
        score = list(map(int, input().split(" ")))
        galton_list.append(score)

    E = 0
    for i in range(h):
        E_part = 0
        for j in range(len(galton_list[i])):
            E_part += galton_list[i][j] * all_pascal_lines[i][j]
        E += E_part * 2 ** (h - i - 1)
    E = int(E)
    M = 2 ** (h - 1)
    ans[set_n] = [frac(E, M).numerator, frac(E, M).denominator]
    # print(ans[set_n][0], ans[set_n][1])

for set_n in range(set_count):
    print(ans[set_n][0], ans[set_n][1])
