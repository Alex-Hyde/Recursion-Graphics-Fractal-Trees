# --------------------------------------------------------------------
# Program: Vector classes
# Author: Alex Hyde
# Date: Oct 25 2019
# Description: Classes for easy processing and storing of 2D and 3D
#   vectors
# --------------------------------------------------------------------

import math


# 3 dimensional vector
class Vec3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get(self, i=False):
        if i:
            return int(self.x), int(self.y), int(self.z)
        return self.x, self.y, self.z

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other):
        return Vec3(self.x // other, self.y // other, self.z // other)

    def __sub__(self, point):
        return Vec3(self.x - point.x, self.y - point.y, self.z - point.z)

    def __add__(self, point):
        return Vec3(self.x + point.x, self.y + point.y, self.z + point.z)

    def __mul__(self, cons):
        return Vec3(self.x * cons, self.y * cons, self.z * cons)

    # dot product
    def dot(self, point):
        return self.x * point.x + self.y * point.y + self.z * point.z

    # cross product
    def cross(self, other):
        return Vec3(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

    def distance(self, point):
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    # unit vector
    def unit(self):
        length = len(self)
        return Vec3(self.x/length, self.y/length, self.x/length)

    def __str__(self):
        return str(self.x) + " ," + str(self.y) + " ," + str(self.z)


# 2 dimensional vector
class Vec2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self, i=False):
        if i:
            return int(self.x), int(self.y)
        return self.x, self.y

    def __truediv__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vec2(self.x // other, self.y // other)

    def __sub__(self, point):
        return Vec2(self.x - point.x, self.y - point.y)

    def __add__(self, point):
        return Vec2(self.x + point.x, self.y + point.y)

    def __mul__(self, cons):
        return Vec2(self.x * cons, self.y * cons)

    # dot product
    def dot(self, point):
        return self.x * point.x + self.y * point.y

    def distance(self, point):
        return math.sqrt((point.x - self.x) ** 2 + (point.y - self.y) ** 2)

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # unit vector
    def unit(self):
        length = len(self)
        return Vec2(self.x/length, self.y/length)

    def __str__(self):
        return str(self.x) + " ," + str(self.y)

    # slope between two 2D vectors
    def slope(self, other):
        if other.x - self.x == 0:
            return 1000000000
        return (other.y - self.y) / (other.x - self.x)

    # angle between two 3D vectors
    def angle(self, other):
        angle = math.degrees(math.atan((other.y - self.y)/(other.x - self.x+0.000000001)))
        if other.x < self.x:
            return angle + 180
        if other.y < self.y:
            return angle + 360
        return angle

    def get_point_on_line(self, angle, dis=1):
        x = self.x + dis * math.cos(math.radians(angle))
        y = self.y + dis * math.sin(math.radians(angle))
        return Vec2(x, y)

    # y int of vector and slope
    def y_int(self, slope):
        return self.y - slope * self.x

    # closest point to a line (represented by two points on that line)
    @staticmethod
    def closest_point(a, b, p):
        slope = a.slope(b)
        p2 = Vec2(p.x + 1, p.y - slope)
        return Vec2.poi(a, b, p, p2)

    # point of intersection between 2 lines (represented by two points on that line)
    @staticmethod
    def poi(a1, a2, b1, b2):
        m1 = a2.slope(a1)
        m2 = b2.slope(b1)
        d1 = a1.y_int(m1)
        d2 = b1.y_int(m2)

        x = (d2 - d1) / (m1 - m2 + 0.00000001)
        y = m1 * x + d1

        return Vec2(x, y)

    @staticmethod
    def poi_slope(a, m1, b, m2):
        d1 = a.y_int(m1)
        d2 = b.y_int(m2)

        x = (d2 - d1) / (m1 - m2)
        y = m1 * x + d1

        return Vec2(x, y)
