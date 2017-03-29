import mathutils
from mathutils import Vector

class Point(Vector):
    def __init__(self, *args, **kwargs):
        super(Point, self).__init__(*args, **kwargs)

class Transform(mathutils.Matrix):
    def __init__(self, *args, **kwargs):
        super(Transform, self).__init__(*args, **kwargs)

    def __pow__(self, exp):
        if exp < 1:
            return self.Identity(4)
        result = self.Identity(4)
        count  = self
        while exp:
            if exp % 2 == 1:
                result = result * count
            count = count * count
            exp = exp // 2
        return result

