from math import atan2, pi


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_on_line(self, line):   # p1 and p2 - Points that define line
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

    def intersects(self, other):    # other - Segment
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

    def sq_len(self):
        ln = self.x * self.x + self.y * self.y
        return ln

    def len(self):
        return self.sq_len() ** 0.5

    def add(self, other):
        x = self.x + other.x
        y = self.y + other.y
        p = Point(x, y)
        return Vector(p)

    def mul(self, a):
        x = self.x * a
        y = self.y * a
        p = Point(x, y)
        return Vector(p)

    def div(self, a):
        return self.mul(1 / a)

    def reverse(self):
        p = Point(-self.x, -self.y)
        return Vector(p)


class Polygon:
    def __init__(self, vertices: list):  # vertices - list of Points
        self.vertices = vertices
        self.vert_cnt = len(vertices)
        self.perimeter = self.get_perimeter()
        self.area = self.get_area()

    def get_perimeter(self):
        temp_list = self.vertices + [self.vertices[0]]
        per = 0
        for i in range(len(temp_list) - 1):
            p1 = temp_list[i]
            p2 = temp_list[i + 1]
            v = Vector(p1, p2)
            per += v.len()
        return per

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
    #angle2 = atan2(b.y, b.x)
    #angle1 = atan2(a.y, a.x)
    #angle = (angle2 - angle1) % pi
    angle = atan2(cross_product(a, b), dot_product(a, b))
    return angle


def sign(x):
    if x > 0:
        return 1
    return -1 if x < 0 else 0


A = Point(0, 0)
B = Point(0, 2)
C = Point(2, 2)
D = Point(2, 0)
E = Point(2, -2)
F = Point(1, 1)

A2 = Point(0, 0)
B2 = Point(0, 2)
C2 = Point(0, 2)
D2 = Point(0, 1)

# 1. точка на прямой
line = Line(A, B)
print(A.is_on_line(line))

# 2. пересечение отрезков
s1 = Segment(A, B)
s2 = Segment(C, D)
print(s1.intersects(s2))
s1 = Segment(A2, B2)
s2 = Segment(C2, D2)
print("2 parallel segments", s1.intersects(s2))

# 3. принадлежность полигону
points = [D, A, B, C]
poly = Polygon(points)
print(poly.contains(F))

# 4. площадь полигона
poly2 = Polygon([A, B, C, D, E])
print(poly2.area)

# точка на отрезке
print(A.is_on_segment(s1))

# проверка способов
a = Vector(Point(54.45, 7.556), Point(-74.55, 41.32))
b = Vector(Point(77.36, -8.56), Point(-7.55, -8.32))
print(angle_between(a, b))
print(atan2(cross_product(a, b), dot_product(a, b)))
a = Vector(Point(0, 0), Point(-1, -0.1))
b = Vector(Point(0, 0), Point(-1, 0.1))
print(angle_between(a, b))
print(atan2(cross_product(a, b), dot_product(a, b)))

p1 = Point(0, 0)
p2 = Point(0, 10)
p3 = Point(10, 10)
p4 = Point(10, 0)

poly = Polygon([p1, p2, p3, p4])
print(poly.contains(Point(66, 15204)))

