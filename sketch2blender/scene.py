import math

from geometry import Vector, Point, Transform

class Dots(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = points

class Line(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = points

class Curve(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = points

class Polygon(object):
    def __init__(self, options, points):
        self.opts = options
        self.points = points

class Sweep(object):
    def __init__(self, slices, closed, transforms, swept):
        self.slices = slices
        self.closed = closed
        self.transforms = transforms
        self.swept = swept

class Repeat(object):
    def __init__(self, count, transforms, repeated):
        self.n = count
        self.transforms = transforms
        self.repeated = repeated

class Compound(object):
    def __init__(self, transform, child):
        self.transform = transform
        self.child = child

class Special(object):
    # TODO(david): don't need this, really
    def __init__(self, code, args, line):
        self.code = code
        self.args = args
        self.line = line

