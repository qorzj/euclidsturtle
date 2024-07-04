import math


def float_equals(f1, f2):
    return math.isclose(f1, f2, rel_tol=0.01) or abs(f1 - f2) < 0.02


def float_tuple_equals(tp1, tp2):
    return float_equals(tp1[0], tp2[0]) and float_equals(tp1[1], tp2[1])


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.start = (x1, y1)
        self.end = (x2, y2)

    def intersection_point(self, other: 'Segment'):
        """
        get (x, y) of intersection point of two segments
        return (None, None) if not intersected
        """
        x1, y1 = self.start
        x2, y2 = self.end
        x3, y3 = other.start
        x4, y4 = other.end
        # Calculate the intersection point using the formula for two lines
        den = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        if den == 0:
            return None, None  # The segments are parallel
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) -
             (x1 - x2) * (x3 * y4 - y3 * x4)) / den
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) -
             (y1 - y2) * (x3 * y4 - y3 * x4)) / den
        if min(x1, x2) <= x <= max(x1, x2) and min(x3, x4) <= x <= max(x3, x4):
            return x, y
        else:
            return None, None

    @staticmethod
    def get_segments(lines):
        segments = []
        for i in range(len(lines) - 1):
            segments.append(Segment(*lines[i], *lines[i + 1]))
        return segments

    @staticmethod
    def intersection_existed(segments1, segments2, ignore_point=None):
        for s1 in segments1:
            for s2 in segments2:
                x, y = s1.intersection_point(s2)
                if x is not None and (ignore_point is None or not float_tuple_equals((x, y), ignore_point)):
                    return True
        return False


class Line:
    """
    Line for ax+by=c
    """

    def __init__(self, segment: Segment):
        """
        Init from a segment
        """
        x1, y1 = segment.start
        x2, y2 = segment.end
        self.a = y2 - y1
        self.b = x1 - x2
        self.c = x1 * y2 - x2 * y1

    def intersection_point(self, other: 'Line'):
        """
        get (x, y) of intersection point of two lines
        return (None, None) if not intersected
        """
        determinant = self.a * other.b - other.a * self.b
        if float_equals(determinant, 0):
            return None, None  # Lines are parallel, no intersection
        x = (other.b * self.c - self.b * other.c) / determinant
        y = (self.a * other.c - other.a * self.c) / determinant
        return x, y


def get_middividing_point(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 + x2) / 2, (y1 + y2) / 2


def get_centralsymmetry_point(p, center):
    x, y = p
    cx, cy = center
    return 2 * cx - x, 2 * cy - y


def get_axialsymmetry_point(p, axis: Line):
    x1, y1 = p
    a, b, c = axis.a, axis.b, axis.c
    return ((b*b-a*a)*x1-2*a*b*y1+2*a*c)/(a*a+b*b), ((a*a-b*b)*y1-2*a*b*x1+2*b*c)/(a*a+b*b)


def get_axialsymmetry_angle(p_angle, axis_angle):
    angle = 2 * axis_angle - p_angle
    if angle < 0:
        angle += 360
    elif angle >= 360:
        angle -= 360
    return angle
