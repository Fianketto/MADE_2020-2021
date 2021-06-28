import sys
from math import atan2, pi


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_on_line(self, line):  # p1 and p2 - Points that define line
        v1 = Vector(self, line.p1)
        v2 = Vector(self, line.p2)
        return cross_product(v1, v2) == 0

    def is_on_segment(self, s):  # s - Segment
        if not self.is_on_line(Line(s.start, s.end)):
            return False
        dx1 = self.x - s.start.x
        dx2 = self.x - s.end.x
        dy1 = self.y - s.start.y
        dy2 = self.y - s.end.y
        if sign(dx1) != sign(dx2) or sign(dy1) != sign(dy2):
            return True
        return False


class Segment:
    def __init__(self, a: Point, b: Point):
        self.start = a
        self.end = b


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


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

    def contains(self, p: Point, include_border=True):
        if include_border:
            return self._contains_on_border(p) or self._contains_inside(p)
        return not self._contains_on_border(p) and self._contains_inside(p)

    def _contains_inside(self, p: Point):
        EPS = 0.5
        total_angle = 0
        for i in range(self.vert_cnt):
            vertex1 = self.vertices[i]
            vertex2 = self.vertices[(i + 1) % self.vert_cnt]
            vector1 = Vector(p, vertex1)
            vector2 = Vector(p, vertex2)
            angle = angle_between(vector1, vector2)
            total_angle += angle
        return abs(total_angle) > EPS

    def _contains_on_border(self, p: Point):
        point_is_on_side = False
        for i in range(self.vert_cnt):
            vertex1 = self.vertices[i]
            vertex2 = self.vertices[(i + 1) % self.vert_cnt]
            side = Segment(vertex1, vertex2)
            if p.is_on_segment(side):
                point_is_on_side = True
                break
        return point_is_on_side


def dot_product(a: Vector, b: Vector):
    product = a.x * b.x + a.y * b.y
    return product


def cross_product(a: Vector, b: Vector):
    product = a.x * b.y - a.y * b.x
    return product


def angle_between(a: Vector, b: Vector):
    angle = atan2(cross_product(a, b), dot_product(a, b))
    return angle


def sign(x):
    if x > 0:
        return 1
    return -1 if x < 0 else 0


n, x, y = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
vertex_list = [None for i in range(n)]
p = Point(x, y)

i = 0
for input_line in sys.stdin.buffer.read().decode().splitlines():
    a = list(input_line.split())
    v = Point(int(a[0]), int(a[1]))
    vertex_list[i] = v
    i += 1

poly = Polygon(vertex_list)

if poly.contains(p):
    print("YES")
else:
    print("NO")

"""
4 6
0 0
0 0
0 10
10 10
10 0
0 0
10 10
5 5
-1 10
66 15204

4 1
0 0
0 10
10 10
10 0
5 5

20 20
"""
