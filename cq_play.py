from cq_shortcuts import *
from math import sin, cos, pi

SEGMENTS = 48


width = 14
height = 14
offset = 3


def row(z=30, xoffset=3, yoffset=3):
    keys = []
    for i in range(4):
        x = i * (width + xoffset)
        key = wp().box(width, height, 4)
        keys.append([[x, 0, z], [x + width, 0, z], [x + width, height, z], [x, height, z]])
        wp().transformed(cq.Vector())

    return keys


def sinusoidal_ring(rad=25, segments=SEGMENTS):
    outline = []
    for i in range(segments):
        angle = i * 2 * pi / segments
        x = rad * (cos(angle) + i / segments)
        y = rad * sin(angle)
        z = 2 * rad * (sin(angle) / 5 + i / segments)
        outline.append((x, y, z))
    return outline


def triangle(base=15, ratio=2):
    return [(-base / 2, 0), (base / 2, 0), (0, base * ratio)]


def extrude_example():
    shape = triangle()
    path = sinusoidal_ring(rad=50)
    p = cq.Workplane("XY").spline(path, includeCurrent=True)
    s = cq.Workplane("YZ").polyline(shape).close().sweep(p)
    return s


result = wp('XY').box(10, 10, 1).faces(">Z").rect(3, 3).workplane(offset=5).circle(3).loft().faces(">Z").edges().fillet(0.4)
show_object(result)
