import math
import turtle

from .geotool import Segment, float_tuple_equals, get_centralsymmetry_point


class Turtle(turtle.Turtle):
    def __getitem__(self, index):
        t = Turtle()
        if isinstance(index, slice):
            points = self.currentLine[index]
            self.teleport(points[0])
            for point in points[1:]:
                self.go_towards(point)
        else:
            t.setheading(self.heading())
            t.teleport(self.currentLine[index])
        return t

    def __len__(self):
        return len(self.currentLine)

    def setscale(self, scale=1.0):
        screen = self.getscreen()
        screen.xscale = screen.yscale = scale

    def disappear(self):
        self.reset()
        self.hideturtle()

    def length(self):
        total_distance = 0
        start = self.currentLine[0]
        for point in self.currentLine[1:]:
            total_distance += math.dist(start, point)
            start = point
        return total_distance

    def teleport(self, x, y=None):
        speed = self.speed()
        self.speed(0)
        self.goto(x, y)
        self.clear()
        self.speed(speed)

    def into_shell(self):
        self.dot(5)
        self.hideturtle()

    def go_towards(self, target, percent=100):
        if isinstance(target, tuple):
            target_pos = target
        else:
            target_pos = target.position()
        self.setheading(self.towards(target_pos))
        if percent == 100:
            self.goto(target_pos)
        else:
            x1, y1 = self.position()
            x2, y2 = target_pos
            x, y = x1 + (x2 - x1) * percent / 100, y1 + \
                (y2 - y1) * percent / 100
            self.goto(x, y)

    def parallel(self, v, opposite=False):
        if opposite:
            self.setheading((v.heading() + 180) % 360)
        else:
            self.setheading(v.heading())

    def axial_symmetry(self, axis, line=False):
        pass

    def central_symmetry(self, center, line=False):
        if not line:
            x, y = get_centralsymmetry_point(
                self.position(), center.position())
            t = self[-1]
            t.teleport(x, y)
            t.left(180)
            return t
        else:
            points = self.currentLine
            t = self[0]
            t.left(180)
            t.teleport(get_centralsymmetry_point(points[0], center.position()))
            for point in points[1:]:
                t.go_towards(get_centralsymmetry_point(
                    point, center.position()))
            return t

    def axis(self, v):
        pass

    def smart_forward(self):
        segments = []
        segments.extend(self._screen_borders())
        for t in turtle.turtles():
            if t.isvisible():
                segments.extend(Segment.get_segments(t.currentLine))
        r = self[-1]
        r.color('#CCCCCC')
        r.speed(0)
        # lb, ub = 0, 10000.0  # lower bound and upper bound
        lb, ub = 0, 500 / self.getscreen().xscale  # lower bound and upper bound
        while ub - lb > 0.01:
            mid = (lb + ub) / 2
            # print(f'lb={lb}, ub={ub}, mid={mid}')
            r.forward(mid)
            r_segment = Segment(*self.position(), *r.position())
            intersected = False
            for s in segments:
                x, y = s.intersection_point(r_segment)
                # if x is not None:
                #     print(f'intersected at ({x}, {y}) {self.position()}')
                if x is not None and not float_tuple_equals((x, y), self.position()):
                    intersected = True
                    break
            if intersected:
                ub = mid
            else:
                lb = mid
            r.undo()
        r.disappear()
        self.forward(ub)

    def smart_circle(self, radius):
        segments = []
        for t in turtle.turtles():
            if t.isvisible():
                segments.extend(Segment.get_segments(t.currentLine))
        r = self[-1]
        r.color('#CCCCCC')
        r.speed(0)
        lb, ub = 0, 720.0  # lower bound and upper bound
        while ub - lb > 0.5:
            mid = (lb + ub) / 2
            r.circle(radius, mid)
            r_segments = Segment.get_segments(r.currentLine)
            if Segment.intersection_existed(segments, r_segments, ignore_point=self.position()):
                ub = mid
            elif mid == 360:
                ub = lb = mid
            else:
                lb = mid
            r.undo()
        r.disappear()
        if ub >= 30:
            self.circle(radius, ub, int(ub / 10))
        else:
            self.circle(radius, ub)

    def _screen_borders(self):
        screen = self.getscreen()
        screen_width = screen.window_width() / screen.xscale
        screen_height = screen.window_height() / screen.yscale
        return [
            Segment(-screen_width / 2, -screen_height / 2,
                    screen_width / 2, -screen_height / 2),
            Segment(screen_width / 2, -screen_height / 2,
                    screen_width / 2, screen_height / 2),
            Segment(screen_width / 2, screen_height / 2, -
                    screen_width / 2, screen_height / 2),
            Segment(-screen_width / 2, screen_height / 2, -
                    screen_width / 2, -screen_height / 2)
        ]


Pen = Turtle
