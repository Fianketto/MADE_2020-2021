import sys


def get_index(c):
    return ord(c) - FIRST_LETTER_ORD


class Node:
    def __init__(self):
        self.dict_size = 0
        self.links = [None for i in range(LETTER_COUNT)]
        self.is_terminal = False

    def show(self):
        return self.links


class Tree:
    def __init__(self):
        self.root = Node()

    def add(self, s, add_from):
        i = get_index(s[0])
        if add_from.links[i] is not None:
            next_node = add_from.links[i]
        else:
            next_node = Node()
            add_from.links[i] = next_node
        next_part = None if len(s) == 1 else s[1:]
        if next_part is not None:
            self.add(next_part, next_node)
        else:
            next_node.is_terminal = True
        return

    def consists(self, s, search_from):
        i = get_index(s[0])
        if search_from.links[i] is None:
            return False
        next_node = search_from.links[i]
        if len(s) == 1:
            if next_node.is_terminal:
                return True
            return False
        else:
            next_part = s[1:]
            return self.consists(next_part, next_node)


WORD_MAX_LENGTH = 30
LETTER_COUNT = 26
FIRST_LETTER_ORD = ord('a')


s = sys.stdin.buffer.readline().decode().strip()
m = int(sys.stdin.buffer.readline().decode())
words = ['' for i in range(m)]
ans = ['No' for i in range(m)]
words_found = set()

i = 0
for line in sys.stdin.buffer.read().decode().splitlines():
    words[i] = line.strip()
    i += 1

sl = len(s)
tree = Tree()

for word in words:
    tree.add(word, tree.root)

for i in range(sl):
    for j in range(1, min(WORD_MAX_LENGTH + 1, sl - i + 1)):
        p = s[i: i + j]
        if tree.consists(p, tree.root):
            words_found.add(p)

for i in range(m):
    if words[i] in words_found:
        ans[i] = 'Yes'

sys.stdout.buffer.write(("\n".join(ans) + "\n").encode())

'''
trololo
29
t
tr
tro
trol
trolo
trolol
trololo
r
ro
rol
rolo
rolol
rololo
o
ol
olo
olol
ololo
l
lo
lol
lolo
o
ol
olo
l
lo
o
troll
'''