from jupyter_cadquery.viewer.client import show_object
from cq_shortcuts import *
from params import *


def screw_hole():
    return wp().cylinder(sm_screw_depth, sm_screw_dia_btm / 2)


def sensor_mount():
    sm_base = wp().box(sm_base_w, sm_base_h, sm_base_d).rotate((0, 0, 0), (0, 0, 1), 90).edges("|Z").fillet(8.0)
    bottom_hole = wp().box(4, 4, 6).translate((0, -2, 0)).union(wp().cylinder(6, 2))

    result = sm_base.cut(bottom_hole).translate((0, 0, sm_offset_z))
    result = rotate_around_z(result, 180)
    return result


def btu(bearings=False):

    def btu_base():
        return wp().cylinder(btu_base_depth_calc, btu_base_dia_calc / 2)

    def btu_head():
        return wp().cylinder(btu_base_depth_calc + btu_ball_height_calc, btu_head_dia_calc / 2)

    def btu_ball():
        return wp().sphere(btu_ball_dia / 2)

    b = btu_base()\
        .union(btu_head().translate((0, 0, btu_base_depth_calc)))\
        .union(btu_ball().translate((0, 0, (btu_ball_z_offset_calc + btu_head_depth_calc) * -1)))

    if bearings:
        b.cut(bearing_cutter())

    return b


def btus(bearings=False):
    result = None
    for i in range(3):
        a = i * PI3
        b = btu(bearings)
        b = rotate_around_x(b, btu_tilt)
        b = rotate_around_z(b, math.degrees(-a))
        x = btu_ring_r * math.sin(a)
        y = btu_ring_r * math.cos(a)
        b = b.translate((x, y, -10.9))

        result = result.union(b) if result is not None else b

    return result


def top_plate():
    tp_thickness = 5
    tp_rim_size = 1.5
    tp_clearance = 0.6
    _tp_hole_r_top = math.exp(math.log(math.exp(math.log(ball_diameter / 2) * 2) - 
                                       math.exp(math.log(tp_thickness) * 2)) * 0.5) + tp_clearance
    _tp_hole_r_btn = (ball_diameter / 2) + (tp_clearance * 2)

    result = wp().cylinder(tp_thickness, skt_dia / 2)\
        .union(wp().cylinder(tp_rim_size, (skt_dia + tp_rim_size + 1) / 2).translate((0, 0, 3.5)))
    result = result.cut(wp().cylinder(tp_thickness + 1, _tp_hole_r_top / 2).translate((0, 0, -0.5)))
    return result


def coords(angle, dist):
    x = math.sin(angle) * dist
    y = math.cos(angle) * dist
    return x, y


def fin(width, length, corner_radius,):
    sphere = wp().sphere(width / 2)
    return sphere


# def fin(width, length, corner_radius,):
#     x1, y1 = coords(0, length)
#     x2, y2 = coords(PI3, length)
#     x3, y3 = coords(PI3 * 2, length)
#     plane = cq.Workplane("front").moveTo(x1, y1).lineTo(x2, y2).lineTo(x3, y3).close().extrude(width)
#     plane = plane.edges("|Z").fillet(corner_radius)
#     plane = plane.translate((0, 0, -width/2))
#     return plane


def bearing_cutter():
    cutter = wp().cylinder(3.3, 4).translate((1.7, 0, 0))
    axle_groove = wp().box(4, 3.1, 8).edges(">X").fillet(0.8).translate((1.2, 0, 0))
    return cutter.union(axle_groove)


def bearing_fin(with_cut=False):
    axle_radius = 3
    axle_width = 9
    base_fin = fin(13, 9, axle_radius)

    if with_cut:
        # cutter = wp().cylinder(3.3, 4).translate((1.7, 0, 0))
        # axle_groove = wp().box(4, 3.1, 8).edges(">X").fillet(0.8).translate((1.2, 0, 0))
        base_fin = base_fin.cut(bearing_cutter())

    return base_fin


def fins(with_cut=False):
    rots = [90, -30, 210]
    # rots = [120, 0, 240]
    radius_offset = -2
    result = []
    ball = wp().sphere(padded_ball_radius)
    for i in range(3):
        b_fin = bearing_fin(with_cut)
        radians = i * (PI2 / 3)
        # degrees = 90 + (i * 120)
        x = math.sin(radians) * (ball_radius + radius_offset)
        y = math.cos(radians) * (ball_radius + radius_offset)

        b_fin = rotate_around_x(b_fin, 90)
        b_fin = rotate_around_y(b_fin, 35)
        b_fin = rotate_around_z(b_fin, rots[i])
        b_fin = b_fin.translate((x, y, -12))
        b_fin = b_fin.cut(ball)
        result.append(b_fin)

    return result


slot_inner_radius = 20
slot_outer_radius = 23.5
slot_angle = 30


def flanges():
    flange_pos = [
        75, 165, 295
    ]
    flange_offset = -1.80
    shape = None
    for angle in flange_pos:
        flange = arc(angle + 120, 30, slot_inner_radius, slot_outer_radius, height=0.9)
        flange = flange.edges(">Z").chamfer(0.2)
        shape = shape.union(flange) if shape is not None else flange

    return shape.translate((0, 0, flange_offset))


def generate_base_socket():
    ball = wp().sphere(padded_ball_radius)
    bottom_cutter = wp().box(sm_base_w * 2, sm_base_h * 2, sm_base_d * 3).rotate((0, 0, 0), (0, 0, 1), math.pi / 2) \
        .translate((0, 0, -(19.8 + (sm_base_d / 2))))
    box_cutter = wp().box(socket_radius * 2 + ball_padding, socket_radius * 2 + ball_padding, socket_radius * 2) \
        .translate((0, 0, socket_radius)).union(ball)

    inner_cyl = wp().cylinder(5, padded_ball_radius)
    top_cyl = wp().cylinder(5, socket_radius).cut(inner_cyl).translate((0, 0, 2.5))
    lip = wp().cylinder(1.25, socket_radius + 1.5).cut(cq.Workplane("XY").cylinder(1.25, ball_radius + 0.1)).translate(
        (0, 0, 5.5))
    lip = lip.edges("<Z").chamfer(1.0)
    top_cyl = top_cyl.union(lip)

    sm_screw_holes = screw_hole()\
        .translate((0, sm_screw_dist / 2, 0))\
        .union(screw_hole().translate((0, -(sm_screw_dist / 2), 0)))\
        .translate((0, 0, sm_offset_z - 2.0))

    socket = wp().sphere(socket_radius)  # .cut(bottom_cutter)
    sensor = sensor_mount()
    socket = socket.cut(bottom_cutter.union(ball))
    sensor = sensor.cut(ball)
    sensor = sensor.translate((0, 0, 0.1))
    socket = socket.union(sensor)
    socket = socket.cut(sm_screw_holes)
    socket = rotate_around_x(socket, -5)
    socket = socket.union(top_plate())
    socket = socket.cut(box_cutter)
    socket = socket.union(top_cyl)
    socket = socket.union(flanges())
    return socket


def generate_btu_socket():

    socket = generate_base_socket()
    socket = socket.cut(btus())

    socket = rotate_around_z(socket, -90)

    return socket


def generate_bearing_socket():

    socket = generate_base_socket()
    for b_fin in fins():
        socket = socket.cut(b_fin)
    for b_fin in fins(True):
        socket = socket.union(b_fin)

    socket = rotate_around_z(socket, -90)

    return socket


# Render the solid
show_object(generate_bearing_socket())
