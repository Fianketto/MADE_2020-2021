import decimal

p = 35184372089371
set_count = int(input())
ans = [0 for i in range(set_count)]

for i in range(set_count):
    x = int(input())
    n = (-1 + pow(1 + 8 * x, 0.5)) / 2
    n_int = float(int(n))
    if n_int < n:
        n = n_int + 1
    s = 1 + 0.5 * (n * n - n)
    k = x - s
    # print("k=", k)
    # ans0 = (pow(2, n) + pow(2, k)) % p
    a1 = pow(2, int(k), p)
    a2 = pow(2, int(n - k), p)
    ans1 = (a1 * (a2 + 1)) % p
    ans[i] = ans1

for i in range(set_count):
    print(ans[i])
