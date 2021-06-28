import sys


def get_hash(my_hash, l, r):
    if l == 0:
        return my_hash[r]
    return (my_hash[r] - (my_hash[l - 1] * powp[r - l + 1])) % M


def initialize_hash(s):
    my_hash = [0 for i in range(len(s))]
    my_hash[0] = ord(s[0])
    for i in range(1, len(s)):
        my_hash[i] = (my_hash[i - 1] * P + ord(s[i])) % M
    return my_hash


def hash_intersection(subs_len):
    list_of_hash_sets = []
    for i in range(k):
        new_set = set()
        for j in range(len(words[i]) - subs_len + 1):
            new_set.add(get_hash(all_hashes[i], j, j + subs_len - 1))
        list_of_hash_sets.append(new_set)
    if len(list_of_hash_sets) == 1:
        return list_of_hash_sets[0]
    return list_of_hash_sets[0].intersection(*list_of_hash_sets[1:])


def binary_search(y, left, right):
    hash_int_max = set()
    while left < right - 1:
        m = (left + right) // 2
        hash_int = hash_intersection(m)
        if y <= -1 * len(hash_int):
            right = m
        else:
            left = m
            hash_int_max = hash_int
    return right - 1, hash_int_max


P = 37
M = 2000001

k = int(sys.stdin.buffer.readline().decode())
words = ['' for i in range(k)]
w_lens = [0 for i in range(k)]
all_hashes = []
ans = ''
substring_exists = False

i = 0
for line in sys.stdin.buffer.read().decode().splitlines():
    words[i] = line.strip()
    w_lens[i] = len(words[i])
    i += 1
shortest_word_len = min(w_lens)
longest_word_len = max(w_lens)

powp = [1 for i in range(longest_word_len)]
for i in range(1, longest_word_len):
    powp[i] = (powp[i - 1] * P) % M

for word in words:
    next_hash = initialize_hash(word)
    all_hashes.append(next_hash)

right, hash_int_max = binary_search(0, 0, shortest_word_len + 1)

if right > 0:
    substring_exists = True

if substring_exists:
    words.sort(key=len)
    shortest_word = words[0]
    shortest_word_hash = initialize_hash(shortest_word)
    for i in range(shortest_word_len - right + 1):
        if get_hash(shortest_word_hash, i, i + right - 1) in hash_int_max:
            substring = shortest_word[i: i + right]
            ans = substring

print(ans)

'''
if all(substring in s_curr for s_curr in words[1:]):
    print(substring)
    break
'''

