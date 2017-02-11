class Point2(object):
    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def dist(self, other):
        diff = other - self
        return diff.length()

    def dist_sqr(self, other):
        return diff.length_sqr()

    def lerp(self, other, scale):
        return self + scale * (other - self)

    def __add__(self, other):
        assert type(other) in (Vector2,)
        return Point2(self.x + other.x,
                      self.y + other.y)

    __radd__ = __add__

    def __sub__(self, other):
        assert type(other) in (Point2,)
        return Vector2(self.x - other.x,
                       self.y - other.y)

    def __rsub__(self, other):
        assert type(other) in (Point2,)
        return Vector2(other.x - self.x,
                       other.y - self.y)

    @classmethod
    def origin(cls):
        return cls(0, 0)

class Point3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dist(self, other):
        diff = other - self
        return diff.length()

    def dist_sqr(self, other):
        diff = other - self
        return diff.length_sqr()

    def lerp(self, other, scale):
        return self + scale * (other - self)

    def __add__(self, other):
        assert type(other) in (Vector3,)
        return Point3(self.x + other.x,
                      self.y + other.y,
                      self.z + other.z)

    __radd__ = __add__

    def __sub__(self, other):
        assert type(other) in (Point3,)
        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)

    def __rsub__(self, other):
        assert type(other) in (Point3,)
        return Vector3(other.x - self.x,
                       other.y - self.y,
                       other.z - self.z)

    @classmethod
    def origin(cls):
        return cls(0, 0, 0)

class Polyline2(object):
    def __init__(self, pts=[]):
        self.points = []
        self.next   = None

class Polyline3(object):
    def __init__(self, pts=[]):
        self.points = []
        self.next   = None

class Polygon2(object):
    pass

class Polygon3(object):
    pass

class Vector(list):
    def __init__(self, size=0):
        super().__init__([0.0 for i in range(size)])

    # clear exists

    def setup(self, size):
        self.clear()
        self.extend([0.0 for i in range(size)])

    def zero(self, size):
        self[:size] = [0.0 for i in range(size)]

    # copy exists

class Vector2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return sqrt(self.dot(self))

    def length_sqr(self):
        return self.dot(self)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def unit(self):
        length = self.length()
        if length <= 0.0001: # TODO(david): EPSILON
            return None
        return (1.0/length) * self

    def __add__(self, other):
        assert type(other) in (Vector2,Point2,)
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x,
                           self.y + other.y)
        return other.__add__(self)

    def __radd__(self, other):
        return other.__add__(self)

    def __sub__(self, other):
        assert type(other) in (Vector2,)
        return Vector2(self.x - other.x,
                       self.y - other.y)

    def __rsub__(self, other):
        return other.__sub__(self)

    def __rmul__(self, scalar):
        assert type(scalar) in (int, float)
        return Vector2(scalar * self.x,
                       scalar * self.y)

    __mul__ = __rmul__

    def __inv__(self):
        return -1.0 * self

class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def length(self):
        return sqrt(self.dot(self))

    def length_sqr(self):
        return self.dot(self)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def unit(self):
        length = self.length()
        if length <= 0.0001: # TODO(david): EPSILON
            return None
        return (1.0/length) * self

    def __add__(self, other):
        assert type(other) in (Vector3,Point3,)
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x,
                           self.y + other.y,
                           self.z + other.z)
        return other.__add__(self)

    def __radd__(self, other):
        return other.__add__(self)

    def __sub__(self, other):
        assert type(other) in (Vector3,)
        return Vector3(self.x - other.x,
                       self.y - other.y,
                       self.z - other.z)

    def __rsub__(self, other):
        return other.__sub__(self)

    def __rmul__(self, scalar):
        assert type(scalar) in (int, float)
        return Vector3(scalar * self.x,
                       scalar * self.y,
                       scalar * self.z)

    __mul__ = __rmul__

    def __inv__(self):
        return -1.0 * self

class Vector4(object):
    pass

class Plane(object):
    pass

class Box2(object):
    pass

class Box3(object):
    pass

class Transform(object):
    pass

class Quaternion(object):
    pass

