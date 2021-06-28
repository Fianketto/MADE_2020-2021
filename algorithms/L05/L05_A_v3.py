from sys import stdin, stdout


class Map:
    def __init__(self):
        self.M = 10 ** 6
        self.A = 101
        self.P = 99787
        self.arr = ['' for i in range(self.M)]

    def hash_func(self, k):
        return ((k * self.A) + self.P) % self.M

    def put(self, k):
        h = self.hash_func(k)
        if self.is_free_for_put(h):
            self.arr[h] = k
        else:
            i = 0
            h_next = self.hash_func(k + i)
            while not self.is_free_for_put(h_next):
                if self.arr[h_next] == k:
                    return  # k уже есть
                i += 1
                h_next = self.hash_func(k + i)
            self.arr[h_next] = k

    def exists(self, k):
        i = 0
        h_next = self.hash_func(k + i)
        while not self.is_empty(h_next):
            if self.arr[h_next] == k:
                return "true"
            else:
                i += 1
                h_next = self.hash_func(k + i)
        return "false"

    def delete(self, k):
        i = 0
        h_next = self.hash_func(k + i)
        while not self.is_empty(h_next):
            if self.arr[h_next] == k:
                self.arr[h_next] = 'r'
                # переместить влево оставшиеся по условию!
                break
            else:
                i += 1
                h_next = self.hash_func(k + i)

    def is_free_for_put(self, x):
        if self.arr[x] == '' or self.arr[x] == 'r':
            return True
        return False

    def is_empty(self, x):
        if self.arr[x] == '':
            return True
        return False

    def show(self):
        print(self.arr)


m = Map()
# m.show()
for line in stdin:
    a = list(line.split())
    if a[0][0] == "i":
        m.put(int(a[1]))
        m.show()
    elif a[0][0] == 'd':
        m.delete(int(a[1]))
        m.show()
    else:
        stdout.write(m.exists(int(a[1])) + "\n")
