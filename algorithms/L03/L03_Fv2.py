def func(x):
    c1 = (x ** 2 + (1 - a) ** 2) ** 0.5
    c2 = ((1 - x) ** 2 + a ** 2) ** 0.5
    t = c1 / v1 + c2 / v2
    return t


v1, v2 = list(map(int, input().split()))
a = float(input())
EPS = 10 ** (-5)

left_b = 0
right_b = 1

for i in range(100):
    m1 = (2 * left_b + right_b) / 3
    m2 = (left_b + 2 * right_b) / 3
    if func(m1) < func(m2):
        right_b = m2
    else:
        left_b = m1
    if abs(right_b - left_b) < EPS:
        break

print(left_b)
