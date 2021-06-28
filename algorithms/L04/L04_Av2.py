import sys


def min_of(x, y):
    if x is None:
        return y
    return min(x, y)


class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.min_so_far = None

    def insert(self, x):
        if self.size == 0:
            self.head = Node(x, None)
            self.tail = self.head
        else:
            self.tail.next_node = Node(x, None)
            self.tail = self.tail.next_node
        self.size += 1

    def erase(self):
        if self.size == 1:
            self.head = None
            self.tail = None
        elif self.size == 2:
            self.head.next_node = None
            self.tail = self.head
        else:
            prev = self.head
            curr = prev.next_node
            for i in range(1, self.size - 1):
                prev = curr
                curr = prev.next_node
            prev.next_node = None
            self.tail = prev
        self.size -= 1
        if self.size == 0:
            self.min_so_far = None
        else:
            self.min_so_far = self.tail.data


main_linked_list = LinkedList()
linked_list_of_mins = LinkedList()
n = int(sys.stdin.readline())
ans = [0 for i in range(n)]
ans_count = 0
for i in range(n):
    a = list(map(int, sys.stdin.readline().split()))
    if a[0] == 1:
        min_so_far = min_of(linked_list_of_mins.min_so_far, a[1])
        linked_list_of_mins.min_so_far = min_so_far
        linked_list_of_mins.insert(min_so_far)
        main_linked_list.insert(a[1])
    elif a[0] == 2:
        main_linked_list.erase()
        linked_list_of_mins.erase()
    else:
        ans[ans_count] = linked_list_of_mins.min_so_far
        ans_count += 1

ans = ans[:ans_count]
sys.stdout.write("\n".join(map(str, ans)))
