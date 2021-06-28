def func(x):
    return x ** 2 + x ** 0.5 - c


EPS = 10 ** (-6)
ITER_COUNT = 100
left_b, right_b = 0, 10 ** 5
c = float(input())
x = right_b / 2 + left_b / 2
for i in range(ITER_COUNT):
    y = func(x)
    if abs(y) < EPS:
        break
    elif y > 0:
        right_b = x
    else:
        left_b = x
    x = right_b / 2 + left_b / 2

print(x)
