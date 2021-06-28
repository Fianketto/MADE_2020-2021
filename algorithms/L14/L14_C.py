import sys


def build_p_function(s):
    pr[0] = 0
    for i in range(1, len(s)):
        k = pr[i - 1]
        while k > 0 and s[i] != s[k]:
            k = pr[k - 1]
        if s[i] == s[k]:
            k += 1
        pr[i] = k


def get_entries(j):
    entries = []
    for i in range(len(pr)):
        if pr[i] == j:
            entries.append(str(i - 2 * j + 1))
    return entries


p = input().strip()
t = input().strip()

s = p + "#" + t
pr = [0 for i in range(len(s))]
build_p_function(s)
ans = get_entries(len(p))

print(len(ans))
print(" ".join(ans))
