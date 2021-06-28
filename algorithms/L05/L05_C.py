import sys


# Узел
class Node:
    def __init__(self, the_key, the_value):
        self.the_key = the_key
        self.the_value = the_value
        self.next_node = None
        self.prev_node = None

    def change_value(self, new_value):
        self.the_value = new_value


# Двусвязный список с возможностью удаления узла из середины
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # Вставка узла в конец
    def insert(self, new_node):
        if self.size == 0:
            self.head = self.tail = new_node
        else:
            new_node.prev_node = self.tail
            self.tail.next_node = new_node
            self.tail = new_node
        self.size += 1

    # Удаление узла по ссылке
    def erase(self, node_to_remove):
        if self.size == 0:
            return
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            if node_to_remove is self.head:
                right_node = self.head.next_node
                right_node.prev_node = None
                self.head = right_node
            elif node_to_remove is self.tail:
                left_node = self.tail.prev_node
                left_node.next_node = None
                self.tail = left_node
            else:
                right_node = node_to_remove.next_node
                left_node = node_to_remove.prev_node
                left_node.next_node = right_node
                right_node.prev_node = left_node
        self.size -= 1


class Map:
    def __init__(self):
        self.M = 10 ** 5
        self.P = 10 ** 9
        self.A = 31
        self.arr = [[] for i in range(self.M)]

    def hash_func(self, s):
        res = 0
        for i in range(len(s)):
            res = (res * self.A + ord(s[i])) % self.P
        res %= self.M
        return res

    # Нахождение индексов повторяется во всех функциях ниже
    # Поэтому выделяем в отдельную функцию (-1, если такого ключа нет)
    def get_index(self, k):
        h = self.hash_func(k)
        for i in range(len(self.arr[h])):
            if self.arr[h][i].the_key == k:
                return h, i
        return h, -1

    def put(self, k, v):
        h, i = self.get_index(k)
        if i >= 0:
            self.arr[h][i].change_value(v)
            return
        new_node = Node(k, v)
        self.arr[h].append(new_node)
        linked_list.insert(new_node)

    def delete(self, k):
        h, i = self.get_index(k)
        if i >= 0:
            linked_list.erase(self.arr[h][i])
            del self.arr[h][i]

    def get(self, k):
        h, i = self.get_index(k)
        if i >= 0:
            return self.arr[h][i].the_value
        return "none"

    def get_next(self, k):
        h, i = self.get_index(k)
        if i >= 0 and self.arr[h][i].next_node is not None:
            return self.arr[h][i].next_node.the_value
        return "none"

    def get_prev(self, k):
        h, i = self.get_index(k)
        if i >= 0 and self.arr[h][i].prev_node is not None:
            return self.arr[h][i].prev_node.the_value
        return "none"


m = Map()
linked_list = LinkedList()
ans = []
for line in sys.stdin.buffer.read().decode().splitlines():
    a = list(line.split())
    if a[0] == "put":
        m.put(a[1], a[2])
    elif a[0] == "delete":
        m.delete(a[1])
    elif a[0] == "get":
        ans.append(m.get(a[1]))
    elif a[0] == "prev":
        ans.append(m.get_prev(a[1]))
    elif a[0] == "next":
        ans.append(m.get_next(a[1]))

sys.stdout.buffer.write("\n".join(ans).encode())
