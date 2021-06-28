import sys


class ComplexHashMap:
    """
    Основной класс для реализации MultiMap.
    Помимо основного класса используются еще 2 дополнительных класса:
        1.  Node - стандартный узел для включения в связный список.
            Добавлены 2 новых атрибута (см. далее).
        2.  LinkedList - стандарный связный список (из задачи С).
            Добавлено 2 новых метода (см. далее).
    Основной класс ComplexHashMap сосотит из 2-х внутренних классов:
        1.  MapType2 - стандартный Map (из задач B/C) с разрешением коллизий
            методом цепочек. В этом массиве хранятся списки объектов класса
            Node, для которых индекс h2 определен функцией hash_func(x, y),
            т.е. хеширование происходит по паре значений x, y.
            self.m2 - объект этого класса.
        2.  MapType1 - стандартный Map с разрешением коллизий методом цепочек.
            В этом массиве хранятся списки объектов класса LinkedList. Каждый
            такой объект (связный список) относится к определенному ключу x и
            состоит из узлов, соответствующих всем добавленным парам с первым
            элементом, равным x.
    """

    def __init__(self):
        self.M = 10 ** 5
        self.A = 31
        self.P = 10 ** 9
        self.m1 = self.MapType1(self.M, self.A, self.P)
        self.m2 = self.MapType2(self.M, self.A, self.P)

    class MapType1:
        """
        В объекте данного класса храним список arr.
        В списке arr на позиции h1 храним список из связных списков, каждый
        из которых соответствует такому ключу x, что hash_func(x) = h1.
        """

        def __init__(self, m, a, p):
            self.M = m
            self.A = a
            self.P = p
            self.arr = [[] for i in range(self.M)]

        # Хеш от первого элемента пары (от ключа)
        def hash_func(self, s):
            res = 0
            for i in range(len(s)):
                res = (res * self.A + ord(s[i])) % self.P
            res %= self.M
            return res

        # Получение индексов для доступа к связному списку, соответствующему
        # первому элементу пары (ключу). Если по такому ключу еще не добавляли
        # связный список, то возвращаем -1
        def get_index(self, k):
            h1 = self.hash_func(k)
            for j in range(len(self.arr[h1])):
                if self.arr[h1][j].the_key == k:
                    return h1, j
            return h1, -1

        # Вставка нового узла в связный список.
        # Если нужного связного списка еще нет, сначала создаем его.
        def put_linked_list(self, k, new_node):
            h1, j = self.get_index(k)
            if j >= 0:
                # если СС с ключом k уже есть, то вставляем в него узел new_node
                self.arr[h1][j].insert(new_node)
                return
            # иначе создаем новый СС и вставляем new_node уже в новый СС
            new_linked_list = LinkedList(k)
            self.arr[h1].append(new_linked_list)
            new_linked_list.insert(new_node)

        # Получение всех данных из связного списка на позиции h1, j
        def get_all_nodes(self, h1, j):
            values = self.arr[h1][j].get_all_values()
            return str(self.arr[h1][j].size) + " " + values

    class MapType2:
        """
        В объекте данного класса храним список arr.
        В списке arr на позиции h2 храним список из узлов, каждый
        из которых соответствует такой паре x,y, что hash_func(x, y) = h2.
        """

        def __init__(self, m, a, p):
            self.M = m
            self.A = a
            self.P = p
            self.arr = [[] for i in range(self.M)]

        # Каждый узел "знает", на какой позиции он находится в списке
        # arr[h2]. Но при удалении какого-либо элемента из массива arr[h2]
        # индексы следующих элементов уменьшатся на 1. Чтобы сохранить
        # "знания", требуется внести поправку для каждого такого элемента.
        def fix_index(self, h2, index):
            for i in range(index, len(self.arr[h2])):
                self.arr[h2][i].index -= 1

        # Хеш от пары элементов
        def hash_func(self, s1, s2=""):
            res = 0
            s = s1 + "_" + s2
            for i in range(len(s)):
                res = (res * self.A + ord(s[i])) % self.P
            res %= self.M
            return res

        # Получение индексов для доступа к узлу, соответствующему паре
        # элементов x, y (или k, v) Если по такой паре еще не добавляли
        # узел, то возвращаем -1
        def get_index(self, k, v):
            h2 = self.hash_func(k, v)
            for i in range(len(self.arr[h2])):
                if self.arr[h2][i].the_key == k and self.arr[h2][i].the_value == v:
                    return h2, i
            return h2, -1

        # Вставка нового узла
        def put(self, k, v, m1):
            h2, i = self.get_index(k, v)
            if i >= 0:
                return
            new_node = Node(k, v, h2, len(self.arr[h2]))
            self.arr[h2].append(new_node)
            m1.put_linked_list(k, new_node)

        # Удаление узла
        def delete(self, k, v, m1):
            h2, i = self.get_index(k, v)
            if i >= 0:
                h1, j = m1.get_index(k)
                node_to_remove = self.arr[h2][i]
                m1.arr[h1][j].erase(node_to_remove)
                if m1.arr[h1][j].size == 0:
                    del m1.arr[h1][j]
                del self.arr[h2][i]
                self.fix_index(h2, i)

    # Вставка пары элементов
    def put(self, x, y):
        self.m2.put(x, y, self.m1)

    # Удаление пары элементов
    def delete(self, x, y):
        self.m2.delete(x, y, self.m1)

    # Получение всех пар с первым элементом x
    def get_all(self, x):
        h1, j = self.m1.get_index(x)
        if j < 0:
            return '0'
        return self.m1.get_all_nodes(h1, j)

    # Удаление всех пар с первым элементом x
    def delete_all(self, x):
        h1, j = self.m1.get_index(x)
        if j < 0:
            return
        self.m1.arr[h1][j].delete_all_nodes(self.m2)
        del self.m1.arr[h1][j]


class Node:
    """
    Стандартный узел с добавлением двух новых атрибутов:
        h2 - хеш по паре x, y (key, value). Нужен для быстрого доступа к
        тому списку массива self.m2, в котором находится данный узел.
        index - позиция данного узла в списке, указанном выше.
        Таким образом, доступ к данному узлу имеется как из связного списка
        внутри m1, так и из массива m2 по ссылке m2[h2][index]
    """

    def __init__(self, the_key, the_value, h2, index):
        self.the_key = the_key
        self.the_value = the_value
        self.next_node = None
        self.prev_node = None
        self.h2 = h2
        self.index = index


class LinkedList:
    """
    Двусвязный список с возможностью удаления узла из середины
    """

    def __init__(self, k):
        self.head = None
        self.tail = None
        self.size = 0
        self.the_key = k

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

    # Получение данных с каждого узла связного списка
    def get_all_values(self):
        values = [0] * self.size
        node = self.head
        for i in range(self.size):
            values[i] = node.the_value
            node = node.next_node
        values = " ".join(values)
        return values

    # Удаление всех узлов связного списка
    def delete_all_nodes(self, m2):
        node = self.head
        for _ in range(self.size):
            h2 = node.h2
            i = node.index
            del m2.arr[h2][i]
            m2.fix_index(h2, i)
            node = node.next_node


complex_hash_map = ComplexHashMap()
ans = []
for line in sys.stdin.buffer.read().decode().splitlines():
    a = list(line.split())
    if a[0] == "put":
        complex_hash_map.put(a[1], a[2])
    elif a[0] == "delete":
        complex_hash_map.delete(a[1], a[2])
    elif a[0] == "deleteall":
        complex_hash_map.delete_all(a[1])
    elif a[0] == "get":
        ans.append(complex_hash_map.get_all(a[1]))

sys.stdout.buffer.write("\n".join(ans).encode())
