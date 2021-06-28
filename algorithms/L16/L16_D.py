import sys
from math import atan2, pi


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector:
    def __init__(self, a: Point, b: Point = None):
        if b is None:
            self.x = a.x
            self.y = a.y
        else:
            self.x = b.x - a.x
            self.y = b.y - a.y


class Polygon:
    def __init__(self, vertices: list):  # vertices - list of Points
        self.vertices = vertices
        self.vert_cnt = len(vertices)
        self.area = self.get_area()

    def get_area(self):
        area = 0
        vertex0 = self.vertices[0]
        for i in range(1, self.vert_cnt - 1):
            vertex1 = self.vertices[i]
            vertex2 = self.vertices[i + 1]
            a = Vector(vertex0, vertex1)
            b = Vector(vertex0, vertex2)
            product = cross_product(a, b)
            area += product
        area = abs(area) / 2
        return area


def cross_product(a: Vector, b: Vector):
    product = a.x * b.y - a.y * b.x
    return product


n = int(sys.stdin.buffer.readline().decode())
vertex_list = [None for i in range(n)]

i = 0
for input_line in sys.stdin.buffer.read().decode().splitlines():
    a = list(input_line.split())
    p = Point(int(a[0]), int(a[1]))
    vertex_list[i] = p
    i += 1

poly = Polygon(vertex_list)
print(poly.area)
