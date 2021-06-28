def prefix_func(s, x):
    s_plus_x = x + '#' + s
    p = [0] * len(s_plus_x)
    for i in range(1, len(s_plus_x)):
        k = p[i - 1]
        while k > 0 and s_plus_x[k] != s_plus_x[i]:
            k = p[k - 1]
        if s_plus_x[k] == s_plus_x[i]:
            k += 1
        p[i] = k
    return p


st_1 = input()
st_2 = input()
print(st_1, len(st_1))

prefix = prefix_func(st_2, st_1)
# print(prefix)
ans = 0
ans_2 = []
for j in range(len(st_2)):
    if prefix[len(st_1) + 1 + j] == len(st_1):
        ans += 1
        ans_2.append(j - 1)

print(ans)
print(*ans_2)