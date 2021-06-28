def build_z_function(s):
    l, r = 0, 0
    n = len(s)
    z = [0 for i in range(n)]
    for i in range(1, n):
        z[i] = max(0, min(r - i, z[i - l]))
        while i +z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l = i
            r = i + z[i]
    for i in range(len(z)):
        z[i] = str(z[i])
    return z


s = input().strip()
z = build_z_function(s)
print(" ".join(z[1:]))
