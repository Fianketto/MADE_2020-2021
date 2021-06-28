import sys


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

    def intersects(self, other):  # other - Segment
        ab = Vector(self.start, self.end)
        ac = Vector(self.start, other.start)
        ad = Vector(self.start, other.end)

        cd = Vector(other.start, other.end)
        ca = Vector(other.start, self.start)
        cb = Vector(other.start, self.end)

        s1 = sign(cross_product(ab, ac))
        s2 = sign(cross_product(ab, ad))
        s3 = sign(cross_product(cd, ca))
        s4 = sign(cross_product(cd, cb))
        if abs(s1) + abs(s2) + abs(s3) + abs(s4) == 0:
            segment_cd = Segment(other.start, other.end)
            return self.start.is_on_segment(segment_cd) or self.end.is_on_segment(segment_cd)
        return s1 != s2 and s3 != s4


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


def dot_product(a: Vector, b: Vector):
    product = a.x * b.x + a.y * b.y
    return product


def cross_product(a: Vector, b: Vector):
    product = a.x * b.y - a.y * b.x
    return product


def sign(x):
    if x > 0:
        return 1
    return -1 if x < 0 else 0


arr = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
p = Point(arr[0], arr[1])
a = Point(arr[2], arr[3])
b = Point(arr[4], arr[5])
seg = Segment(a, b)

if p.is_on_segment(seg):
    print("YES")
else:
    print("NO")
