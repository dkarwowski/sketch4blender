import math

from copy import deepcopy

from geometry import Vector, Point, Transform

class Tag(object):
    pass

class Dots(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Dots(" + repr(self.points) + ")"

class Line(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Line(" + repr(self.points) + ")"

class Curve(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Curve(" + repr(self.points) + ")"

class Polygon(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Polygon(" + repr(self.points) + ")"

class Sweep(object):
    def __init__(self, options, slices, closed, transforms, swept):
        self.opts = options
        self.slices = slices
        self.closed = closed
        self.transforms = transforms
        self.swept = deepcopy(swept)

    def __repr__(self):
        return "Sweep(" + repr(self.slices) + ", " + repr(self.closed) + ", " + repr(self.swept) + ")"

class Repeat(object):
    def __init__(self, count, transforms, repeated):
        self.n = count
        self.transforms = transforms
        self.repeated = deepcopy(repeated)

    def __repr__(self):
        return "Repeat(" + repr(self.repeated) + ", " + repr(self.n) + ")"

class Compound(object):
    def __init__(self, transform, child):
        self.transform = transform
        self.child = deepcopy(child)

    def __repr__(self):
        return "Compound(" + repr(self.child) + ")"

class Special(object):
    # TODO(david): don't need this, really
    def __init__(self, code, args, line):
        self.code = code
        self.args = args
        self.line = line

