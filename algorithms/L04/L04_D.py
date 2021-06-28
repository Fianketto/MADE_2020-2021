import sys


class Heap:
    def __init__(self):
        # id_orders - список, содержащий на i-ом месте позицию операции i в списке elements.
        # Нумерация операций с 0, поэтому при выводе прибавляем 1.
        # Если операция i уже извлечена или не является push, храним "-1"
        self.capacity = 1
        self.size = 0
        self.elements = [''] * self.capacity
        self.id_orders = []

    def push(self, value, operation_id):
        if self.size == self.capacity:
            self.expand_list()
        i = self.size
        self.elements[i] = [value, operation_id]
        self.id_orders.append(self.size)
        self.size += 1
        self.go_up(i)

    def extract_min(self):
        if self.size == 0:
            return "*\n"
        min_element = self.elements[0]
        self.swap(0, self.size - 1)
        self.size -= 1
        self.go_down(0)
        self.id_orders[min_element[1]] = -1
        return str(min_element[0]) + " " + str(min_element[1] + 1) + "\n"

    def go_up(self, i):
        # Поднимаем элемент i вверх по куче, пока он меньше родителя
        while i > 0 and self.elements[i][0] < self.elements[(i - 1) // 2][0]:
            self.swap(i, (i - 1) // 2)
            i = (i - 1) // 2

    def go_down(self, i):
        # Опускаем элемент i вниз по куче, пока он больше детей
        while 2 * i + 1 < self.size:
            cur = self.elements[i][0]
            left = self.elements[2 * i + 1][0]
            if 2 * i + 2 == self.size:
                right = float('inf')
            else:
                right = self.elements[2 * i + 2][0]
            if left >= cur and right >= cur:
                break
            elif left <= right and left <= cur:
                self.swap(i, 2 * i + 1)
                i = 2 * i + 1
            elif right <= left and right <= cur:
                self.swap(i, 2 * i + 2)
                i = 2 * i + 2

    def swap(self, x, y):
        self.elements[x], self.elements[y] = self.elements[y], self.elements[x]
        x, y = self.elements[x][1], self.elements[y][1]
        self.id_orders[x], self.id_orders[y] = self.id_orders[y], self.id_orders[x]

    def expand_list(self):
        self.capacity *= 2
        temp_elements = [''] * self.capacity
        for i in range(self.size):
            temp_elements[i] = self.elements[i]
        self.elements = temp_elements

    def decrease_key(self, operation_id, new_value):
        if self.id_orders[operation_id] >= 0:
            self.elements[self.id_orders[operation_id]][0] = new_value
            self.go_up(self.id_orders[operation_id])


h = Heap()
operation_cnt = 0
for line in sys.stdin:
    a = list(line.split())
    if a[0][0] == 'p':
        h.push(int(a[1]), operation_cnt)
    elif a[0][0] == 'e':
        sys.stdout.write(h.extract_min())
        h.id_orders.append(-1)
    else:
        h.decrease_key(int(a[1]) - 1, int(a[2]))
        h.id_orders.append(-1)
    operation_cnt += 1

"""
print(q.size, "/", q.capacity, "\t", q.elements)
for i in range(100):
    a = list(input().split())
    if int(a[0]) == 1:
        q.push(int(a[1]), int(a[2]))
    else:
        print("min: ", q.extract_min())
    print(q.size, "/", q.capacity, "\t", q.elements)
"""

'''
push 54
push 44
push -89
push 56
push 777
extract-min
extract-min


push 3
push 4
push 2
push 1
extract-min
decrease-key 1 -10
extract-min
extract-min
extract-min
extract-min

'''
