from geometry import Transform, Box3
from options  import Opts
from copy     import copy

def bits(num):
    return 1 << num

class GlobalEnv(object):
    EXTENT   = bits(0)
    BASELINE = bits(1)
    OPTS     = bits(2)
    FRAME    = bits(3)
    SPLIT    = bits(4)
    CAMERA   = bits(8)
    LANGUAGE = bits(9)

    def __init__(self):
        self.set_mask = 0
        self.camera   = Transform.identity()
        self.bb1      = Point3.origin()
        self.bb2      = Point3.origin()
        self.opts     = Opts()
        self.frame    = ""
        self.language = 0
        self.baseline = 0.0

    def is_set_p(self, num):
        return self.set_mask & bits(num)

    def check_set_p(flag):
        def decorator(func):
            def wrapper(self, *args, **kwargs):
                if self.is_set_p(flag):
                    return
                self.set_mask |= flag
                func(*args, **kwargs)
            return wrapper
        return decorator

    @check_set_p(bits(OPTS))
    def set_opts(self, opts, line):
        self.opts.setup(opts, line)

    @check_set_p(bits(BASELINE))
    def set_baseline(self, baseline, line):
        if baseline == None:
            return
        self.baseline = baseline

    @check_set_p(bits(EXTENT))
    def set_extent(self, p1, p2, line):
        self.bb1 = copy(p1)
        self.bb2 = copy(p2)

    @check_set_p(bits(CAMERA))
    def set_camera(self, camera, line):
        self.camera = camera

    @check_set_p(bits(FRAME))
    def set_frame(self, opts, line):
        self.frame = opts

    @check_set_p(bits(LANGUAGE))
    def set_output_language(self, lang, line):
        self.language = lang

    def get_transformed_extent(self):
        if self.is_set_p(self.EXTENT):
            return None

        extent = Box3()
        if self.is_set_p(self.CAMERA):
            for i in range(8):


