import math
import cadquery as cq
import numpy
from scipy.spatial import ConvexHull as sphull

PI2 = math.pi * 2
PI3 = PI2 / 3
PI6 = PI3 / 2


def wp(orient="XY"):
    return cq.Workplane(orient)


def box(width, length, height, centered=True):
    return wp().box(width, length, height, centered)


def rotate(shape, angles):
    if angles[0] != 0:
        shape = rotate_around_x(shape, angles[0])
    if angles[1] != 0:
        shape = rotate_around_y(shape, angles[1])
    if angles[2] != 0:
        shape = rotate_around_z(shape, angles[2])

    return shape


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


def face_from_points(points):
    # debugprint('face_from_points()')
    edges = []
    num_pnts = len(points)
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % num_pnts]
        edges.append(
            cq.Edge.makeLine(
                cq.Vector(p1[0], p1[1], p1[2]),
                cq.Vector(p2[0], p2[1], p2[2]),
            )
        )

    face = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges))

    return face


def hull_from_points(points):
    # debugprint('hull_from_points()')
    hull_calc = sphull(points)
    n_faces = len(hull_calc.simplices)

    faces = []
    for i in range(n_faces):
        face_items = hull_calc.simplices[i]
        fpnts = []
        for item in face_items:
            fpnts.append(points[item])
        faces.append(face_from_points(fpnts))

    shape = cq.Solid.makeSolid(cq.Shell.makeShell(faces))
    shape = cq.Workplane('XY').union(shape)
    return shape


def hull_from_shapes(shapes, points=None):
    # debugprint('hull_from_shapes()')
    vertices = []
    for shape in shapes:
        verts = shape.vertices()
        for vert in verts.objects:
            vertices.append(numpy.array(vert.toTuple()))
    if points is not None:
        for point in points:
            vertices.append(numpy.array(point))

    shape = hull_from_points(vertices)
    return shape
