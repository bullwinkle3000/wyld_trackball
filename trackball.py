# from jupyter_cadquery.viewer.client import show_object
from build123d import *
from build123d import *
import cadquery as cq
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
set_port(3939)

from cq_shortcuts import *
# from cq_warehouse.thread import IsoThread

cutout_margin = 0.5
size = (10 - cutout_margin * 2, 10 - cutout_margin * 2)
cutter_radius = 3.175/2

# Ball data
ball_padding = 1.5
ball_diameter = 34
ball_radius = ball_diameter / 2

PI2 = math.pi * 2
PI3 = PI2 / 3
PI6 = PI3 / 2

# socket
socket_clearance = 1
socket_wall_thickness = 4

socket_hole_diameter = ball_diameter + (ball_padding * 2)
socket_diameter = socket_hole_diameter + (socket_wall_thickness * 2)

padded_ball_radius = socket_hole_diameter / 2
socket_radius = socket_diameter / 2

# Sensor mount data
sm_screw_dist = 24
sm_screw_dia_top = 3.1
sm_screw_dia_btm = 2.8
sm_screw_mgn = 1.1
sm_screw_dpth = 8
sm_screw_cap_dia = sm_screw_mgn + sm_screw_dia_btm

sm_base_h = 21
sm_base_l = 28.25
sm_skt_dia = 9
sm_base_d = 1.5
sm_skt_z_offset = 2.6
sm_rot_z = 0

sm_lens_l = 21.4
sm_lens_w = 19
sm_lens_d = 3.5

_sm_base_w = sm_screw_dist + ((sm_screw_dia_top + sm_screw_mgn) * 2)
sm_lens_x = (_sm_base_w - sm_lens_l) / 2
sm_lens_y = (sm_base_h - sm_lens_w) / 2
sm_lens_z = 5.2

sm_offset_z = -18

## BTU
_skt_hole_dia = ball_diameter + (socket_clearance * 2)

btu_color = "white"  ## The color of rendered BTUs
btu_hle_tol = 0.25  ## The tolerance around the BTU for the holes
btu_base_dia = 12.7  ## The diameter of the stem of the BTU
btu_base_dpth = 8  ## The depth of the stem of the BTU
btu_head_dia = 14.5  ## The diameter of the head portion of the BTU
btu_head_dpth = 1  ## The depth of the head portion of the BTU
btu_ball_dia = 8.4  ## The diameter of the ball in the BTU
btu_ball_z_offset = -0.2  ## The z-offset of the BTU ball off the head
btu_z_mult = 1.3

btu_count = 3
btu_tilt = 61
btu_ring_z = 6.3

_btu_base_dia = btu_base_dia + (btu_hle_tol * 2)
_btu_base_dpth = btu_base_dpth + btu_hle_tol

_btu_head_dia = btu_head_dia + (btu_hle_tol * 2)
_btu_head_dpth = btu_head_dpth + btu_hle_tol
_btu_ball_z_offset = btu_ball_dia * btu_ball_z_offset
_btu_head_top = _btu_base_dpth + _btu_head_dpth
_btu_ball_height = (btu_ball_dia / 2) - _btu_ball_z_offset

# btu_ring_r = (_skt_hole_dia / 2) + (_btu_ball_height - 1) / 2
btu_ring_r = 17.5
btu_z_offset = -6.9

bottom_rotate = -10

def screw_hole():
    return wp().cylinder(sm_screw_dpth, sm_screw_dia_btm / 2)


def sensor_mount():
    sm_base = wp().box(_sm_base_w, sm_base_h, sm_base_d).rotate((0, 0, 0), (0, 0, 1), 90).edges("|Z").fillet(8.0)
    bottom_hole = wp().box(4, 4, 6).translate((0, -2, 0)).union(wp().cylinder(6, 2)).rotate((0, 0, 0), (0, 0, 1), 180)

    result = sm_base.cut(bottom_hole).translate((0, 0, sm_offset_z))
    result = rotate_around_z(result, 180)
    return result


def btu():
    def btu_base():
        return wp().cylinder(_btu_base_dpth, _btu_base_dia / 2)

    def btu_head():
        return wp().cylinder(_btu_base_dpth + _btu_ball_height, _btu_head_dia / 2)

    def btu_ball():
        return wp().sphere(btu_ball_dia / 2)

    return btu_base()\
        .union(btu_head().translate((0, 0, _btu_base_dpth)))\
        .union(btu_ball().translate((0, 0, (_btu_ball_z_offset + _btu_head_dpth) * -1)))





def btu_mounts():
    result = None

    for i in range(3):
        a = i * PI3
        b = wp().cylinder(4, 8.5)
        b = b.cut(wp().cylinder(6, 5))
        b = rotate_around_z(b, 90)
        b = rotate_around_x(b, btu_tilt)
        b = rotate_around_z(b, math.degrees(-a))
        x = (btu_ring_r - 2) * math.sin(a)
        y = (btu_ring_r - 2) * math.cos(a)
        b = b.translate((x, y, btu_z_offset + 1.3))
        result = result.union(b) if result is not None else b

    return result


def btus():
    result = None

    for i in range(3):
        a = i * PI3
        b = rotate_around_z(btu(), 90)
        b = rotate_around_x(b, btu_tilt)
        b = rotate_around_z(b, math.degrees(-a))
        x = (btu_ring_r + 0.5) * math.sin(a)
        y = (btu_ring_r + 0.5) * math.cos(a)
        b = b.translate((x, y, btu_z_offset))
        result = result.union(b) if result is not None else b

    return result  # rotate_around_z(result, 30)

def ceramic_bearings():
    result = None

    for i in range(3):
        a = i * PI3
        b = rotate_around_z(wp().cylinder(3, 1.52), 90)
        # b = rotate_around_z(wp().sphere(1.52), 90)
        b = rotate_around_x(b, btu_tilt)
        b = rotate_around_z(b, math.degrees(-a))
        x = (btu_ring_r + 0.5) * math.sin(a)
        y = (btu_ring_r + 0.5) * math.cos(a)
        b = b.translate((x, y, btu_z_offset))
        result = result.union(b) if result is not None else b

    return rotate_around_x(result, bottom_rotate)


def top_plate():
    tp_thickness = 5
    tp_rim_size = 1.5
    tp_clearance = 0.6
    _tp_hole_r_top = math.exp(math.log(math.exp(math.log(ball_diameter / 2) * 2) - math.exp(math.log(tp_thickness) * 2)) * 0.5) + tp_clearance
    _tp_hole_r_btn = (ball_diameter / 2) + (tp_clearance * 2)

    result = wp().cylinder(tp_thickness, socket_radius / 2)\
        .union(wp().cylinder(tp_rim_size, (socket_diameter + tp_rim_size + 1) / 2).translate((0, 0, 3.5)))
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
    flange_offset = -1.63  # -1.68  -1.75
    shape = None
    for angle in flange_pos:
        flange = arc(angle + 120, 30, slot_inner_radius, slot_outer_radius, height=0.9)
        flange = flange.edges(">Z").chamfer(0.2)
        shape = shape.union(flange) if shape is not None else flange


    return shape.translate((0, 0, flange_offset))

thread_depth = 2
MM = 1
IN = 25.4 * MM


# def screw_thread(d, p, ln, ex, hand):
#     return IsoThread(
#         major_diameter=d,
#         pitch=p,
#         length=ln,
#         external=ex,
#         end_finishes=("fade", "square"),
#         hand=hand,
#     )

def access_holes():
    result = None
    for i in range(3):
        a = (PI3 / 2) + (i * PI3)
        b = rotate_around_z(wp().cylinder(10, 7), 90)
        # b = rotate_around_z(wp().sphere(1.52), 90)
        b = rotate_around_x(b, btu_tilt)
        b = rotate_around_z(b, math.degrees(-a))
        x = (btu_ring_r + 0.5) * math.sin(a)
        y = (btu_ring_r + 0.5) * math.cos(a)
        b = b.translate((x, y, btu_z_offset))
        result = result.union(b) if result is not None else b

    return rotate_around_x(result, bottom_rotate / 2)

def generate_cap():
    inner_cyl = wp().cylinder(5, padded_ball_radius).translate((0, 0, 2.5))
    thread_cyl = wp().cylinder(5, padded_ball_radius + thread_depth).translate((0, 0, -2.5))
    top_cyl = cq.Solid.makeCone(socket_radius, socket_radius + 2, 5)
    top_cyl = top_cyl.cut(inner_cyl).cut(thread_cyl).translate((0, 0, 3.0))
    # lip = wp().cylinder(1.5, socket_radius + 1.5).cut(cq.Workplane("XY").cylinder(2, ball_radius + 0.2)).translate((0, 0, 5.5))
    # lip = wp().cylinder(1.25, socket_radius + 2).cut(cq.Workplane("XY").cylinder(1.25, ball_radius - 0.1)).translate(
    #     (0, 0, 5.5))
    # lip = lip.edges("<Z").chamfer(1.2)
    # top_cyl = top_cyl.union(lip)

    # internal_thread = screw_thread(((padded_ball_radius + thread_depth) * MM * 2), MM * 1.5, MM * 3, False, "left")

    # top_cyl = top_cyl.union(internal_thread)

    # iso_external = iso_external_thread.cq_object.fuse(iso_external_core.val())
    return top_cyl


def screw_base():
    inner_wall_cut = wp().cylinder(4, padded_ball_radius).translate((0, 0, 0))

    return wp().cylinder(3, socket_radius).cut(inner_wall_cut).translate((0, 0, 1.4))  # .edges(">Z").fillet(0.6)
    # top_cyl = top_cyl.edges().fillet(0.6)
    # lip = wp().cylinder(1.5, socket_radius + 1.5).cut(cq.Workplane("XY").cylinder(2, ball_radius + 0.2)).translate((0, 0, 5.5))
    # lip = wp().cylinder(1.25, socket_radius + 2).cut(cq.Workplane("XY").cylinder(1.25, ball_radius - 0.1)).translate(
    #     (0, 0, 5.5))
    
    # return top_cyl.cut(inner_wall_cut)

def generate_screw_top():
    # top_ring_cutter = wp().cylinder(5, socket_radius + 1).cut(
    #     wp().cylinder(5, padded_ball_radius + thread_depth - 1.5)).translate((0, 0, 2.5))
    
    # top_cone = cq.Solid.makeCone(socket_radius + 2, socket_radius, 5)
        

    inner_wall_cut = wp().cylinder(2, padded_ball_radius).translate((0, 0, -1))
    # inner_wall_cut.location.position = (0, 0, -1)
    # inner_cyl = Cylinder(2, padded_ball_radius - 1.25)
    # inner_cyl.location.position = (0, 0, 2)
    inner_cyl = wp().cylinder(2, padded_ball_radius - 1.25).translate((0, 0, 1))
    # top_cone.cut(inner_cyl)
    # top_cone.location.position = (0, 0, 1.4)
    top_cyl = wp().cylinder(4, socket_radius + 1).edges(">Z").chamfer(3)
    top_cyl = top_cyl.cut(inner_cyl).cut(inner_wall_cut).translate((0, 0, 1.4)).edges(">Z").fillet(0.6)
    # top_cyl = wp().cylinder(5, socket_radius).edges(">Z").chamfer(1)
    # lip = wp().cylinder(1.5, socket_radius + 1.5).cut(cq.Workplane("XY").cylinder(2, ball_radius + 0.2)).translate((0, 0, 5.5))
    lip = wp().cylinder(1.25, socket_radius + 2).cut(cq.Workplane("XY").cylinder(1.25, ball_radius - 0.1)).translate(
        (0, 0, 5.5))
    # lip = lip.edges("<Z").chamfer(1.2)
    # iso_external_thread = IsoThread(43, 2.5, 2.5)
    # external_thread = screw_thread(((padded_ball_radius + thread_depth) * MM * 2) - 1, MM * 1.5, MM * 3, True, "left")

        # 43,   # (padded_ball_radius + thread_depth + 1) * MM * 2,
        # 2.5,  # * MM,
        # 2.5 * MM).translate((0, 0, 2.1))
    # top_cyl = top_cyl.union(external_thread)
    return top_cyl


def generate_base_socket():
    ball = wp().sphere(padded_ball_radius)
    bottom_cutter = wp().box(_sm_base_w * 2, sm_base_h * 2, sm_base_d * 4).rotate((0, 0, 0), (0, 0, 1), math.pi / 2) \
        .translate((0, 0, -(19.5 + (sm_base_d / 2))))
    box_cutter = wp().box(socket_radius * 2 + ball_padding * 4, socket_radius * 2 + ball_padding * 4, socket_radius * 2) \
        .translate((0, 0, socket_radius)).union(ball)

    # top_ring_cutter = wp().cylinder(5, socket_radius).cut(wp().cylinder(5, padded_ball_radius + thread_depth)).translate((0, 0, 2.5))
    # inner_cyl = wp().cylinder(5, padded_ball_radius)
    top_cyl = generate_screw_top().translate((0, 0, 5))
    # # lip = wp().cylinder(1.5, socket_radius + 1.5).cut(cq.Workplane("XY").cylinder(2, ball_radius + 0.2)).translate((0, 0, 5.5))
    # lip = wp().cylinder(1.25, socket_radius + 2).cut(cq.Workplane("XY").cylinder(1.25, ball_radius - 0.1)).translate(
    #     (0, 0, 5.5))
    # # lip = lip.edges("<Z").chamfer(1.2)
    # iso_external_thread = IsoThread(
    #     major_diameter=(padded_ball_radius + thread_depth + 1) * MM * 2,
    #     pitch=2.5 * MM,
    #     length=2.5 * MM,
    #     external=True,
    #     end_finishes=("fade", "square"),
    #     hand="left",
    # ).translate((0, 0, 2.1))
    # top_cyl = top_cyl.union(iso_external_thread)

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
    socket = rotate_around_x(socket, bottom_rotate)
    socket = socket.union(top_plate())
    socket = socket.cut(box_cutter)
    socket = socket.union(top_cyl)
    socket = socket.union(screw_base())
    # socket = socket.union(flanges())
    return socket


def generate_btu_socket():

    socket = generate_base_socket()
    socket = socket.union(btu_mounts())
    socket = socket.cut(btus())
    socket = rotate_around_z(socket, -90)

    return socket


def generate_ceramic_socket():

    socket = generate_base_socket()
    # socket = socket.union(btu_mounts())
    socket = socket.cut(ceramic_bearings())
    socket = socket.cut(access_holes())
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

# outer_ring = wp().cylinder(5, 23).cut(
#         wp().cylinder(6, 20)).translate((0, 0, 2.5))
#
# inner_ring = wp().cylinder(5, 18).cut(
#         wp().cylinder(6, 16)).translate((0, 0, 2.5))
# inner = inner_ring.union(screw_thread(39, 2.5, 5, True, "right")).translate((0, 0, 10))
# outer = outer_ring.union(screw_thread(40, 2.5, 5, False, "right"))

# show_object(inner.translate((0, 0, 10)))
# show_object(outer)
# show_object(inner)

show_object(generate_ceramic_socket())
# test_123()

# obj = generate_btu_socket()
# show_object(btus())
