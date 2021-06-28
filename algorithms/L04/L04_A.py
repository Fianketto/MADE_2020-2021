import sys


class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert(self, x):
        if self.size == 0:
            self.head = Node(x, None)
            self.tail = self.head
        else:
            new_node = Node(x, self.head)
            self.head = new_node
        self.size += 1

    def erase(self):
        if self.size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next_node
        self.size -= 1


# main_linked_list = LinkedList()
linked_list_of_mins = LinkedList()
n = int(sys.stdin.readline())
for i in range(n):
    a = list(map(int, sys.stdin.readline().split()))
    if a[0] == 1:
        if linked_list_of_mins.size == 0:
            min_so_far = a[1]
        else:
            min_so_far = min(linked_list_of_mins.head.data, a[1])
        linked_list_of_mins.insert(min_so_far)
        # main_linked_list.insert(a[1])
    elif a[0] == 2:
        # main_linked_list.erase()
        linked_list_of_mins.erase()
    else:
        sys.stdout.write(str(linked_list_of_mins.head.data) + "\n")
