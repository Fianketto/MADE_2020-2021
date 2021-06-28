import sys


def get_hash(l, r):
    if l == 0:
        return my_hash[r]
    return (my_hash[r] - (my_hash[l - 1] * powp[r - l + 1])) % M


def initialize_hash(s):
    my_hash[0] = ord(s[0])
    powp[0] = 1
    for i in range(1, len(s)):
        my_hash[i] = (my_hash[i - 1] * P + ord(s[i])) % M
        powp[i] = (powp[i - 1] * P) % M


def compare_substrings(a, b, c, d):
    h1 = get_hash(a, b)
    h2 = get_hash(c, d)
    if h1 == h2:
        return "Yes"
    return "No"


P = 37
M = 2000001


s = sys.stdin.buffer.readline().decode()
m = int(sys.stdin.buffer.readline().decode())
ans = ['' for i in range(m)]
my_hash = [0 for i in range(len(s))]
powp = [0 for i in range(len(s))]
initialize_hash(s)

i = 0
for line in sys.stdin.buffer.read().decode().splitlines():
    a, b, c, d = tuple(map(int, line.split()))
    a, b, c, d = a - 1, b - 1, c - 1, d - 1
    ans[i] = compare_substrings(a, b, c, d)
    i += 1

sys.stdout.buffer.write(("\n".join(ans) + "\n").encode())
