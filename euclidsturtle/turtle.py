import math
import turtle

from .geotool import (Line, Segment, float_tuple_equals,
                      get_axialsymmetry_angle, get_axialsymmetry_point,
                      get_centralsymmetry_point, get_middividing_point)


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
        self.clear()
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
        self.setposition(x, y)
        self.clear()
        self.speed(speed)

    def into_shell(self):
        self.dot(5)
        self.hideturtle()

    def goto(self, target, y=None, *, percent=100):
        if y is not None:
            target_pos = (target, y)
        elif isinstance(target, tuple):
            target_pos = target
        else:
            target_pos = target.position()
        self.setheading(super().towards(target_pos))
        if percent == 100:
            self.setposition(target_pos)
        else:
            x1, y1 = self.position()
            x2, y2 = target_pos
            x, y = x1 + (x2 - x1) * percent / 100, y1 + \
                (y2 - y1) * percent / 100
            self.setposition(x, y)

    def towards(self, target, y=None):
        self.goto(target, y, percent=0)

    def parallel(self, v, *, opposite=False):
        if opposite:
            self.setheading((v.heading() + 180) % 360)
        else:
            self.setheading(v.heading())

    def axial_symmetry(self, axis, *, color=None, line=False):
        axis_start = axis.position()
        axis.forward(100 / self._scale())
        axis_end = axis.position()
        axis.undo()
        axis_line = Line(Segment(*axis_start, *axis_end))
        if not line:
            x, y = get_axialsymmetry_point(self.position(), axis_line)
            t = self[-1]
            if color is not None:
                t.color(color)
            t.teleport(x, y)
            t.setheading(get_axialsymmetry_angle(
                self.heading(), axis.heading()))
            return t
        else:
            points = self.currentLine
            t = self[0]
            if color is not None:
                t.color(color)
            t.setheading(get_axialsymmetry_angle(
                self.heading(), axis.heading()))
            t.teleport(get_axialsymmetry_point(points[0], axis_line))
            for point in points[1:]:
                t.goto(get_axialsymmetry_point(point, axis_line))
            return t

    def central_symmetry(self, center, *, color=None, line=False):
        if not line:
            x, y = get_centralsymmetry_point(
                self.position(), center.position())
            t = self[-1]
            if color is not None:
                t.color(color)
            t.teleport(x, y)
            t.left(180)
            return t
        else:
            points = self.currentLine
            t = self[0]
            if color is not None:
                t.color(color)
            t.left(180)
            t.teleport(get_centralsymmetry_point(points[0], center.position()))
            for point in points[1:]:
                t.goto(get_centralsymmetry_point(point, center.position()))
            return t

    def axis(self, v, *, color=None):
        v_angle = v.heading()
        v_start = v.position()
        v.forward(100 / self._scale())
        v_end = v.position()
        v.undo()
        v_line = Line(Segment(*v_start, *v_end))
        self_angle = self.heading()
        self_start = self.position()
        self.forward(100 / self._scale())
        self_end = self.position()
        self.undo()
        self_line = Line(Segment(*self_start, *self_end))
        its_x, its_y = v_line.intersection_point(self_line)
        if its_x is not None and -10000 < its_x < 10000 and -10000 < its_y < 10000:
            p = (its_x, its_y)
            is_intersected = True
        else:
            p = get_middividing_point(self.position(), v.position())
            while True:
                v_point = get_middividing_point(
                    get_axialsymmetry_point(p, v_line), p)
                self_point = get_middividing_point(
                    get_axialsymmetry_point(p, self_line), p)
                next_p = get_middividing_point(v_point, self_point)
                if float_tuple_equals(p, next_p):
                    break
                p = next_p
            is_intersected = False
        t = Turtle()
        if color is not None:
            t.color(color)
        t.teleport(p)
        if abs(v_angle - self_angle) > 180:
            axis_angle = ((v_angle + self_angle) / 2 + 180) % 360
        else:
            axis_angle = ((v_angle + self_angle) / 2) % 360
        t.setheading(axis_angle)
        if not is_intersected and abs(v_angle - self_angle) > 90:
            t.disappear()
            return t
        front_line = Line(Segment(*self.position(), *v.position()))
        t.forward(100 / self._scale())
        t_line = Line(Segment(*p, *t.position()))
        t.undo()
        t.teleport(t_line.intersection_point(front_line))
        return t

    def smart_forward(self):
        segments = []
        segments.extend(self._screen_borders())
        for t in turtle.turtles():
            if t.isvisible():
                segments.extend(Segment.get_segments(t.currentLine))
        r = self[-1]
        r.color('#CCCCCC')
        r.speed(0)
        lb, ub = 0, 1000 / self._scale()  # lower bound and upper bound
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

    def _scale(self):
        return self.getscreen().xscale


Pen = Turtle
