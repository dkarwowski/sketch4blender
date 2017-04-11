import math

from copy import deepcopy

from .geometry import Vector, Point, Transform

import bpy
import bmesh
from bmesh.types import BMesh, BMVert, BMEdge, BMFace

def _get_gpencil_frame(context):
    S = bpy.context.scene
    if not S.grease_pencil:
        a = [ a for a in bpy.context.screen.areas if a.type == "VIEW_3D" ][0]
        override = {
                'scene' : S,
                'screen' : bpy.context.screen,
                'object' : bpy.context.object,
                'area' : a,
                'region' : a.regions[0],
                'window' : bpy.context.window,
                'active_object' : bpy.context.object,
        }
        print(override)
        bpy.ops.gpencil.data_add(override)

    gp = S.grease_pencil

    if gp.palettes:
        gpp = gp.palettes[0]
    else:
        gpp = gp.palettes.new("test", set_active = True)

    gpc = gpp.colors.new()
    gpc.name = "black"

    if gp.layers:
        gpl = gp.layers[0]
    else:
        gpl = gp.layers.new('gpl', set_active = True)

    if gpl.frames:
        fr = gpl.active_frame if gpl.active_frame else gpl.frames[0]
    else:
        fr = gpl.frames.new(1)

    return fr


class Renderable(object):
    def flatten(self, transform):
        print("no flatten:", repr(self))

    def render_to_blender(self, context):
        print("no to_blender:", repr(self))


class Tag(Renderable):
    def __init__(self):
        super(Tag, self).__init__()


class Dots(Renderable):
    def __init__(self, options, points):
        super(Dots, self).__init__()
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Dots(" + repr(self.points) + ")"

    def flatten(self, transform):
        self.points = [p * transform for p in self.points]

    def render_to_blender(self, context):
        fr = _get_gpencil_frame(context)
        for p in self.points:
            str = fr.strokes.new()
            str.draw_mode = "3DSPACE"

            str.points.add(count = 1)
            str.points[0].co = tuple(p)


class Line(Renderable):
    def __init__(self, options, points):
        super(Line, self).__init__()
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Line(" + repr(self.points) + ")"

    def flatten(self, transform):
        # TODO(david): filter line options properly
        self.points = [p * transform for p in self.points]

    def render_to_blender(self, context):
        fr = _get_gpencil_frame(context)
        str = fr.strokes.new("black")
        str.line_width = 3
        str.draw_mode = "3DSPACE"

        str.points.add(count = len(self.points))
        for i, p in enumerate(self.points):
            str.points[i].co = tuple(p)


class Curve(Renderable):
    def __init__(self, options, points):
        super(Curve, self).__init__()
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Curve(" + repr(self.points) + ")"

    def flatten(self, transform):
        self.points = [p * transform for p in self.points]

    def render_to_blender(self, context):
        fr = _get_gpencil_frame(context)
        str = fr.strokes.new()
        str.line_width = 3
        str.draw_mode = "3DSPACE"

        hermite_points = hermite_3d(self.points)
        str.points.add(count = len(hermite_points))
        for i, p in enumerate(hermite_points):
            str.points[i].co = tuple(p)

def hermite_interp(y, mu, tension=0, bias=0):
    if len(y) != 4:
        return 0.0

    pbias = (1.0 + bias) * (1.0 - tension) / 2.0
    mbias = (1.0 - bias) * (1.0 - tension) / 2.0

    mu2 = mu * mu
    mu3 = mu2 * mu

    m0 = (y[1] - y[0]) * pbias + (y[2] - y[1]) * mbias
    m1 = (y[2] - y[1]) * pbias + (y[3] - y[2]) * mbias

    a0 =  2.0 * mu3 - 3.0 * mu2 + 1.0
    a1 =        mu3 - 2.0 * mu2 + mu
    a2 =        mu3 -       mu2
    a3 = -2.0 * mu3 + 3.0 * mu2

    return a0 * y[1] + a1 * m0 + a2 * m1 + a3 * y[2]

def hermite_3d(pts):
    # extend the points to create full points
    pts = [pts[0]] + pts + [pts[-1]]
    if len(pts) < 4:
        return []

    result = []
    # do this for all consecutive 4
    for i in range(len(pts) - 3):
        xs, ys, zs = zip(*pts[i:i+4])
        # calculate and zip the points to interpolate
        result += list(zip([hermite_interp(xs, mu/10.0) for mu in range(0, 11)],
                           [hermite_interp(ys, mu/10.0) for mu in range(0, 11)],
                           [hermite_interp(zs, mu/10.0) for mu in range(0, 11)]))
    return result


class Polygon(Renderable):
    def __init__(self, options, points):
        super(Polygon, self).__init__()
        self.opts = options
        self.points = deepcopy(points)

    def __repr__(self):
        return "Polygon(" + repr(self.points) + ")"


class Sweep(Renderable):
    def __init__(self, options, slices, closed, transforms, swept):
        super(Sweep, self).__init__()
        self.opts = options
        self.slices = slices
        self.closed = closed
        self.transforms = transforms
        self.swept = deepcopy(swept)

    def __repr__(self):
        return "Sweep(" + repr(self.slices) + ", " + repr(self.closed) + ", " + repr(self.swept) + ")"


class Repeat(Renderable):
    def __init__(self, count, transforms, repeated):
        super(Repeat, self).__init__()
        self.n = count
        self.transforms = transforms
        self.repeated = deepcopy(repeated)

    def __repr__(self):
        return "Repeat(" + repr(self.repeated) + ", " + repr(self.n) + ")"


class Compound(Renderable):
    def __init__(self, transform, child):
        super(Compound, self).__init__()
        self.transform = transform
        self.child = deepcopy(child)

    def __repr__(self):
        return "Compound(" + repr(self.child) + ")"

    def flatten(self, transform):
        transform *= self.transform
        # TODO(david): should flatten return the flattened object?
        #              just in case that this requies a different return
        for c in self.child:
            c.flatten(transform)

    def render_to_blender(self, context):
        for c in self.child:
            print(c)
            c.render_to_blender(context)


class Special(Renderable):
    # TODO(david): don't need this, really
    def __init__(self, code, args, line):
        super(Special, self).__init__()
        self.code = code
        self.args = args
        self.line = line


if __name__=="__main__":
    o = Compount(Transform.Identity(4), Line(None, [Point(1, 2, 3)]))
    o.flatten(Transform.Identity(4))
    o.render_to_blender(None)

