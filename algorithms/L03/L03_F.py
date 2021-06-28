def func(x):
    c1 = (x ** 2 + (1 - a) ** 2) ** 0.5
    c2 = ((1 - x) ** 2 + a ** 2) ** 0.5
    numerator = c2 * x
    denominator = c1 * (1 - x)
    return numerator / denominator - v1 / v2


v1, v2 = list(map(int, input().split()))
a = float(input())
EPS = 10 ** (-5)

left_b = 0
right_b = 1
y = 1
x = right_b / 2 + left_b / 2
for i in range(100):
    y = func(x)
    if abs(y) <= EPS:
        break
    elif y > 0:
        right_b = x
    else:
        left_b = x
    x = right_b / 2 + left_b / 2

print(x)
