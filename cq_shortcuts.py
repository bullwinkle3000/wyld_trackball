import math
import cadquery as cq

PI2 = math.pi * 2
PI3 = PI2 / 3
PI6 = PI3 / 2


def wp(orient="XY"):
    return cq.Workplane(orient)


def rotate_around_x(shape, angle):
    return shape.rotate((0, 0, 0), (1, 0, 0), angle)


def rotate_around_y(shape, angle):
    return shape.rotate((0, 0, 0), (0, 1, 0), angle)


def rotate_around_z(shape, angle):
    return shape.rotate((0, 0, 0), (0, 0, 1), angle)


def point_at(angle, dist):
    return tuple((math.sin(angle) * dist, math.cos(angle) * dist))


def arc(angle, addition, inner_radius, outer_radius, height=1.0):
    a = math.radians(angle)
    mid_a = math.radians(angle + (addition / 2))
    to_a = math.radians(angle + addition)

    inner1 = point_at(a, inner_radius)
    inner2 = point_at(mid_a, inner_radius)
    inner3 = point_at(to_a, inner_radius)

    outer1 = point_at(a, outer_radius)
    outer2 = point_at(mid_a, outer_radius)
    outer3 = point_at(to_a, outer_radius)

    return cq.Workplane("front").moveTo(inner1[0], inner1[1]) \
        .lineTo(outer1[0], outer1[1]) \
        .spline([outer1, outer2, outer3]) \
        .lineTo(inner3[0], inner3[1]) \
        .spline([inner3, inner2, inner1]) \
        .close() \
        .extrude(height)

