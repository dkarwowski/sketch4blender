import mathutils
from mathutils import Vector

class Point(Vector):
    def __init__(self, *args, **kwargs):
        pass
        #super().__init__(*args, **kwargs)

class Transform(mathutils.Matrix):
    def __init__(self, *args, **kwargs):
        pass

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

    @classmethod
    def Scale(cls, factors):
        result = cls.Identity(4)
        result[0][0], result[1][1], result[2][2] = factors
        return result

    @classmethod
    def View(cls, eye, vd, up):
        result = cls.Identity(4)

        unit_vd = vd.normalized()
        unit_up = up.normalized()

        h = unit_vd.cross(unit_up)
        v = h.cross(unit_vd)

        result[0][:3] = h
        result[1][:3] = v
        result[2][:3] = -unit_vd

        result = result.transposed()

        if eye:
            result = result * cls.Translation(-eye)

        return result

