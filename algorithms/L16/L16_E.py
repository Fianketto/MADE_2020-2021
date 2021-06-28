import sys


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

    def sq_len(self):
        ln = self.x * self.x + self.y * self.y
        return ln

    def len(self):
        return self.sq_len() ** 0.5


class Polygon:
    def __init__(self, vertices: list):  # vertices - list of Points
        self.vertices = vertices
        self.vert_cnt = len(vertices)
        self.perimeter = self.get_perimeter()

    def get_perimeter(self):
        temp_list = self.vertices + [self.vertices[0]]
        per = 0
        for i in range(len(temp_list) - 1):
            p1 = temp_list[i]
            p2 = temp_list[i + 1]
            v = Vector(p1, p2)
            per += v.len()
        return per


class PointSet:
    def __init__(self, points: list):  # points - list of Points
        self.points = points
        self.point_cnt = len(points)
        self.points = self.sort_points(self.points)

    @staticmethod
    def sort_points(points, desc=False):
        if not desc:
            points = sorted(points, key=lambda p: p.y)
            points = sorted(points, key=lambda p: p.x)
        else:
            points = sorted(points, key=lambda p: p.y, reverse=True)
            points = sorted(points, key=lambda p: p.x, reverse=True)
        return points

    def build_convex_hull(self):
        a, b = self.points[0], self.points[-1]
        upper_set, lower_set = [a, b], [a, b]

        ab = Vector(a, b)
        for i in range(1, len(self.points) - 1):
            ai = Vector(a, self.points[i])
            if cross_product(ab, ai) >= 0:
                upper_set.append(self.points[i])
            else:
                lower_set.append(self.points[i])

        upper_half = self._build_half_hull(upper_set)
        lower_half = self._build_half_hull(lower_set, desc=True)
        convex_hull_point_list = upper_half + lower_half[1: -1]
        return convex_hull_point_list

    def _build_half_hull(self, set_of_points, desc=False):
        set_of_points = self.sort_points(set_of_points, desc=desc)
        stack = [set_of_points[0]]
        for i in range(1, len(set_of_points)):
            right_turn = False
            p2 = set_of_points[i]
            while not right_turn:
                if len(stack) == 1:
                    stack.append(p2)
                    right_turn = True
                else:
                    p0 = stack[-2]
                    p1 = stack[-1]
                    p0p1 = Vector(p0, p1)
                    p1p2 = Vector(p1, p2)
                    if cross_product(p0p1, p1p2) <= 0:
                        stack.append(p2)
                        right_turn = True
                    else:
                        del stack[-1]
        return stack


def cross_product(a: Vector, b: Vector):
    product = a.x * b.y - a.y * b.x
    return product


def sign(x):
    if x > 0:
        return 1
    return -1 if x < 0 else 0


def can_insert(p):
    ys = point_dict.get(p.x, [])
    if p.y in ys:
        return False
    ys.append(p.y)
    point_dict[p.x] = ys
    return True


n = int(sys.stdin.buffer.readline().decode())
points = [None for i in range(n)]
k = 0
point_dict = {}

i = 0
for input_line in sys.stdin.buffer.read().decode().splitlines():
    a = list(input_line.split())
    p = Point(int(a[0]), int(a[1]))
    if can_insert(p):
        points[i] = p
        i += 1

points = points[:i]
point_set = PointSet(points)

convex_hull_point_list = point_set.build_convex_hull()
convex_hull = Polygon(convex_hull_point_list)

print(convex_hull.perimeter)

