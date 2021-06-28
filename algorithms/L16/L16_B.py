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
        if sign(dx1) != sign(dx2) or sign(dy1) != sign(dy2) or dx1 == dx2 == dy1 == dy2 == 0:
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
            segment_ab = Segment(self.start, self.end)
            on_segment = self.start.is_on_segment(segment_cd) or self.end.is_on_segment(segment_cd)
            on_segment = on_segment or other.start.is_on_segment(segment_ab) or other.end.is_on_segment(segment_ab)
            return on_segment
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


def angle_between(a: Vector, b: Vector):
    angle = atan2(cross_product(a, b), dot_product(a, b))
    return angle


def sign(x):
    if x > 0:
        return 1
    return -1 if x < 0 else 0


# 2. пересечение отрезков
x1, y1, x2, y2 = tuple(map(int, sys.stdin.buffer.readline().decode().split()))
x3, y3, x4, y4 = tuple(map(int, sys.stdin.buffer.readline().decode().split()))

segment1 = Segment(Point(x1, y1), Point(x2, y2))
segment2 = Segment(Point(x3, y3), Point(x4, y4))

if segment1.intersects(segment2):
    print("YES")
else:
    print("NO")
