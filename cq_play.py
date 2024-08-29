from cq_shortcuts import *
from math import sin, cos, pi
from build123d import *
from bd_warehouse.thread import IsoThread
# from ocp_vscode import *
# from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults

# set_port(3939)

SEGMENTS = 48

width = 14
height = 14
offset = 3

lbumps = 30  # number of bumps long
wbumps = 30  # number of bumps wide
thin = True  # True for thin, False for thick

#
# Lego Brick Constants-- these make a Lego brick a Lego :)
#
pitch = 8.0
clearance = 1
bumpDiam = 4.85
bumpHeight = 1.8
if thin:
    height = 3.2
else:
    height = 9.6


def threaded_cylinder():
    thread = IsoThread(major_diameter=8, pitch=1.25, length=20, end_finishes=("fade", "raw"))

    with BuildPart() as rod_end:
        Cylinder(
            thread.min_radius,
            30,
            rotation=(90, 0, 0),
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        )

    return rod_end


def block_bumps(wires):
    t = (pitch - (2 * clearance) - bumpDiam) / 2.0
    postDiam = 6.5  # pitch - t  # works out to 6.5
    total_length = lbumps * pitch - 2.0 * clearance
    total_width = wbumps * pitch - 2.0 * clearance

    # make the base
    # s = cq.Workplane("XY").box(total_length, total_width, height)

    # shell inwards not outwards

    # make the bumps on the top
    s = wp().rarray(pitch, pitch, lbumps, wbumps, True).circle(bumpDiam / 2.0)

    # s = s.intersect(wires)
    return s


def flat_bottom_block():
    #####
    # Inputs
    ######
    lbumps = 2  # number of bumps long
    wbumps = 2  # number of bumps wide
    thin = True  # True for thin, False for thick

    #
    # Lego Brick Constants-- these make a Lego brick a Lego :)
    #
    pitch = 8.0
    clearance = 0.1
    bumpDiam = 4.8
    bumpHeight = 1.8
    if thin:
        height = 2.2
    else:
        height = 9.6

    t = (pitch - (2 * clearance) - bumpDiam) / 2.0
    postDiam = pitch - t  # works out to 6.5
    total_length = lbumps * pitch - 2.0 * clearance
    total_width = wbumps * pitch - 2.0 * clearance

    # make the base
    s = cq.Workplane("XY").box(total_length, total_width, height)
    s = s.edges("|Z").fillet(3)
    s = s.edges("<Z").chamfer(1)
    # shell inwards not outwards
    # s = s.faces("<Z").shell(-1.0 * t)

    # make the bumps on the top
    s = (s.faces(">Z").workplane().
         rarray(pitch, pitch, lbumps, wbumps, True).circle(bumpDiam / 2.0)
         .extrude(bumpHeight))

    # add posts on the bottom. posts are different diameter depending on geometry
    # solid studs for 1 bump, tubes for multiple, none for 1x1
    # tmp = s.faces("<Z").workplane(invert=True)
    #
    # if lbumps > 1 and wbumps > 1:
    #     tmp = (tmp.rarray(pitch, pitch, lbumps - 1, wbumps - 1, center=True).
    #            circle(postDiam / 2.0).circle(bumpDiam / 2.0).extrude(height - t))
    # elif lbumps > 1:
    #     tmp = (tmp.rarray(pitch, pitch, lbumps - 1, 1, center=True).
    #            circle(t).extrude(height - t))
    # elif wbumps > 1:
    #     tmp = (tmp.rarray(pitch, pitch, 1, wbumps - 1, center=True).
    #            circle(t).extrude(height - t))
    # else:
    #     tmp = s

    return s


def blockerize(shape):
    #####
    # Inputs
    ######
    lbumps = 30  # number of bumps long
    wbumps = 30  # number of bumps wide
    thin = True  # True for thin, False for thick

    #
    # Lego Brick Constants-- these make a Lego brick a Lego :)
    #
    pitch = 8.0
    clearance = 1
    bumpDiam = 4.85
    bumpHeight = 1.8
    if thin:
        height = 3.2
    else:
        height = 9.6

    t = (pitch - (2 * clearance) - bumpDiam) / 2.0
    postDiam = 6.5  # pitch - t  # works out to 6.5
    total_length = lbumps * pitch - 2.0 * clearance
    total_width = wbumps * pitch - 2.0 * clearance

    # make the base
    # s = cq.Workplane("XY").box(total_length, total_width, height)

    # shell inwards not outwards
    s = shape.faces("<Z").shell(-1.0 * t)

    # make the bumps on the top
    s = (s.faces(">Z").workplane().
         rarray(pitch, pitch, lbumps, wbumps, True).circle(bumpDiam / 2.0)
         .extrude(bumpHeight))

    # add posts on the bottom. posts are different diameter depending on geometry
    # solid studs for 1 bump, tubes for multiple, none for 1x1
    tmp = s.faces("<Z").workplane(invert=True)

    if lbumps > 1 and wbumps > 1:
        tmp = (tmp.rarray(pitch, pitch, lbumps - 1, wbumps - 1, center=True).
               circle(postDiam / 2.0).circle(bumpDiam / 2.0).extrude(height - t))
    elif lbumps > 1:
        tmp = (tmp.rarray(pitch, pitch, lbumps - 1, 1, center=True).
               circle(t).extrude(height - t))
    elif wbumps > 1:
        tmp = (tmp.rarray(pitch, pitch, 1, wbumps - 1, center=True).
               circle(t).extrude(height - t))
    else:
        tmp = s

    return shape.union(tmp)


def plate_play():
    # shape = wp().cylinder(20, 50, centered=True)
    shape = cq.importers.importStep('./debug_walls_shape.step')
    tool = wp().cylinder(5, 3).translate((0, 50, 0)).union(wp().cylinder(5, 3).translate((0, -50, 0)))
    square = cq.Workplane('XY').rect(1000, 1000)
    for wire in square.wires().objects:
        plane = cq.Workplane('XY').add(cq.Face.makeFromWires(wire))
    shape = shape.intersect(plane)
    outside_arr = shape.vertices(cq.DirectionMinMaxSelector(cq.Vector(1, 0, 0), True)).objects
    outside = outside_arr[0]
    tup = outside.toTuple()
    sizes = []
    max_val = 0
    inner_index = 0
    base_wires = shape.wires().objects
    outer_wire = base_wires[inner_index]
    for i_wire, wire in enumerate(base_wires):
        is_outside = False
        for vert in wire.Vertices():
            vet_tup = vert.toTuple()
            if vet_tup == tup:
                outer_wire = wire
                outer_index = i_wire
                is_outside = True
                sizes.append(0)
        if not is_outside:
            sizes.append(len(wire.Vertices()))
        if sizes[-1] > max_val:
            inner_index = i_wire
            max_val = sizes[-1]
    inner_wire = base_wires[inner_index]
    return block_bumps(inner_wire)
    # inner_shape = cq.Solid.extrudeLinear(outer_wire, [inner_wire], cq.Vector(0, 0, 5))
    # inner_shape = inner_shape.translate((0, 0, -2.5))
    # return inner_shape


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


def insert_46_long_play():
    top_radius = 5.68 / 2
    top_height = 0.55
    medium_radius = 5.5 / 2
    medium_height = 4.5
    medium2_radius = 5.1 / 2
    medium2_height = 0.8
    bottom_radius = 4.85 / 2
    bottom_height = 1.6

    total_height = 6.3
    half_height = total_height / 2

    offset = half_height - (top_height / 2)
    print(offset)
    top = wp().cylinder(top_height, top_radius).translate((0, 0, offset))
    offset -= medium_height / 2
    print(offset)
    medium = wp().cylinder(medium_height, medium_radius).translate((0, 0, offset))
    offset -= medium_height / 2
    offset -= medium2_height / 2
    print(offset)
    medium2 = wp().cylinder(medium2_height, medium2_radius).translate((0, 0, offset))
    offset -= medium2_height / 2
    offset -= bottom_height / 2
    print(offset)
    bottom = wp().cylinder(bottom_height, bottom_radius).translate((0, 0, offset))

    test = wp().cylinder(9, 4.5)
    insert = top.union(medium).union(medium2).union(bottom)
    test = test.cut(insert.translate((0, 0, 4.5 - (total_height / 2))))
    return test


def insert_4_short_play():
    top_radius = 4.7 / 2
    top_height = 2.8
    medium_radius = 4.0 / 2
    medium_height = 1.5
    # medium2_radius = 5.1 / 2
    # medium2_height = 0.8
    # bottom_radius = 4.85 / 2
    # bottom_height = 1.6

    total_height = 4
    half_height = total_height / 2

    offset = half_height - (top_height / 2)
    print(offset)
    top = wp().cylinder(top_height, top_radius).translate((0, 0, offset))
    offset -= top_height / 2
    offset -= medium_height / 2
    print(offset)
    medium = wp().cylinder(medium_height, medium_radius).translate((0, 0, offset))
    offset -= medium_height / 2

    print(offset)

    test = wp().cylinder(6, 4)
    insert = top.union(medium)
    test = test.cut(insert.translate((0, 0, 3 - (total_height / 2))))
    return test


def insert_cutter(radii=(2.35, 2.0), heights=(2.8, 1.5), scale_by=1):
    if len(radii) != len(heights):
        raise Exception("radii and heights collections must have equal length")

    total_height = sum(heights) + 0.2  # add 0.1 for a titch extra

    half_height = total_height / 2
    offset = half_height
    cyl = None
    for i in range(len(radii)):
        radius = radii[i] * scale_by
        height = heights[i]
        offset -= height / 2
        new_cyl = cq.Workplane('XY').cylinder(height, radius).translate((0, 0, offset))
        if cyl is None:
            cyl = new_cyl
        else:
            cyl = cyl.union(new_cyl)
        offset -= height / 2

    return cyl


# result = wp('XY').box(10, 10, 1).faces(">Z").rect(3, 3).workplane(offset=5).circle(3).loft().faces(">Z").edges().fillet(0.4)
# inner = plate_play()
# test = wp().cylinder(6, 4)
#
# test = test.cut(insert_cutter().translate((0, 0, 3 - 2)))

def ball_join():
    sphere = cq.Workplane().sphere(5)
    base = (cq.Workplane(origin=(0, 0, -2))
            .box(12, 12, 10)
            .cut(sphere)
            .edges("|Z")
            .fillet(2)
            )
    sphere_face = base.faces(">>X[2] and (not |Z) and (not |Y)").val()
    base = (base
            .faces("<Z")
            .workplane()
            .circle(2)
            .extrude(10)
            )

    shaft = (cq.Workplane()
             .sphere(4.5)
             .circle(1.5)
             .extrude(20)
             )

    spherical_joint = (base.union(shaft)
                       .faces(">X")
                       .workplane(centerOption="CenterOfMass")
                       .move(0, 4)
                       .slot2D(10, 2, 90)
                       .cutBlind(sphere_face)
                       .workplane(offset=10)
                       .move(0, 2)
                       .circle(0.9)
                       .extrude("next")
                       )

    return spherical_joint


def hand_chair():
    top_len = 90
    top_width = 60
    tl2 = top_len / 2
    tw2 = top_width / 2
    top_height = 10

    side_guard_width = top_width * 2
    side_guard_length = 50
    side_guard_height = top_height

    socket_radius = 12
    socket_tolerance = 0.05

    height = 42

    def make_wall(wall_width, wall_length, wall_height, pos, rot):
        main = wp().box(wall_width, wall_length, wall_height)
        cutout = wp().box((wall_width * 2), wall_length * 2, wall_height).translate(
            ((-wall_width / 2) - 4, 0, wall_height / 2))
        cutout = cutout.faces("<Z").edges().fillet((wall_height / 2) - 1)
        main.faces().edges().fillet(2)
        main = main.cut(cutout)

        main = main.faces(">Z").edges().fillet(1.5)
        # main = main.faces(">Y").edges().fillet(2)
        # main = main.faces(">Y").edges().fillet(1)
        main = rotate(main, rot).translate(pos)
        return main

    def make_guard(sg_width, sg_length, sg_height):
        rotation = 20

        sg_width_2 = sg_width / 2 + 3

        side_offset = 15
        guard_right = wp().box(sg_width_2, sg_length, sg_height).translate((sg_width / 4, 0, 0))

        guard_left = wp().box(sg_width_2, sg_length - side_offset, sg_height).translate((-sg_width / 4, -side_offset / 2, 0))

        guard = guard_right.union(guard_left)

        cutter_right = rotate(wp().box(50, 200, 100).translate((sg_width_2, 0, 0)), (0, 30, -rotation)) # .rotate((0, 0, 1), (0, 0, -1), rotation)
        cutter_left = rotate(wp().box(50, 200, 100).translate((-sg_width_2, 0, 0)), (0, -30, rotation))
        return guard.cut(cutter_right).cut(cutter_left)
        # guard = guard.faces("<Z").edges().fillet(10)

        # return guard  # make_wall(side_guard_length, side_guard_width, side_guard_height, (0, 0, 0), (0, 0, 0))

    def make_top_base():
        pts = [
            (-tw2, tl2),  # top left
            (tw2, tl2),  # top right
            # (tw2, 0),  # mid right
            # (tw2 + side_guard_width, 0),  # top right guard corner
            # (tw2 + side_guard_width, -tl2),  # bottom right
            (-tw2, -tl2),  # bottom left
            (-tw2, tl2)  # top left
        ]

        outline = wp().polyline(pts).close()

        # outline.fillet(2)
        # circ = wp().circle(tw2).translate((0, tl2, 0))
        # outline = outline.union(circ)
        # top = wp().box(top_width, top_len, top_height)
        # top.faces(">X").tag("right")
        # top.faces("<Y").tag("bottom")
        # pad = wp().sphere(30)
        cut_rad = 18  # (top_height + side_guard_height) / 2
        # top = outline.extrude(top_height)

        top = wp().box(top_width, top_len, top_height).translate((0, 0, top_height / 2))
        top = top.faces().edges("|Z").fillet(24)
        # top = top.faces().edges("<X and <Y").fillet(40)
        top = top.faces(">Z").edges().fillet(5)
        top = top.faces("<Z").edges().fillet(3)

        ball = wp().sphere(cut_rad).translate((0, -tl2, 0))
        rod = wp().cylinder(top_len, cut_rad).rotate((-1, 0, 0), (1, 0, 0), 90)
        # rod = rod.translate((-10, 43, 15))
        # ball = ball.translate((-10, 43, 15))
        # rod = rod.union(ball.translate((0, -tl2, 0))).translate((0, tl2 + side_guard_height / 2, side_guard_height / 2))
        # guard = guard.cut(rod)
        # guard = guard.cut(ball)
        # guard = wp().box(side_guard_width, side_guard_length, side_guard_height)
        # guard = wp().cylinder(side_guard_height, side_guard_width / 2)
        # # guard = guard.cut(wp().box(300, 50, 100).translate((0, (-side_guard_width / 2 - 10), 0)))
        # # guard = guard.faces().edges(">Z").fillet(24)
        # guard = guard.faces("<Z").edges().fillet(10)
        # # guard_cutter = box(side_guard_width - 4, side_guard_length * 2, side_guard_height).translate((0, (-side_guard_length / 2) + 53, side_guard_height / 2))
        # guard_cutter = wp().cylinder(side_guard_height, (side_guard_width / 2) - 4).translate(
        #     (0, 0, side_guard_height / 3))
        # # guard_cutter = guard_cutter.faces().edges("|Z").fillet(24)
        # guard_cutter = guard_cutter.faces("<Z").edges().fillet(10)
        # guard = guard.cut(guard_cutter)
        # # guard = guard.rotate((0, 0, 1), (0, 0, -1), 45)
        # guard = guard.faces(">Z").edges().fillet(1.5)
        # guard = guard.cut(wp().box(100, 200, 100).translate((50, 100, 0)))
        # guard = guard.cut(wp().box(100, 200, 100).translate((-50, 80, 0)))
        # # guard = guard.rotate((0, 0, 1), (0, 0, -1), -10)
        # guard = guard.cut(wp().box(300, 50, 100).translate((0, (-side_guard_width / 2) - 5, 0)))
        # guard = guard.translate((0, -top_len / 2 + 35, side_guard_height / 2))
        # guard = guard.faces(">Y").edges().fillet(1.5)
        # guard = guard.faces(">Z").edges(">Y").fillet(10)
        palm_cup = wp().cylinder(2 * (tl2 / 3), 30).rotate((-1, 0, 0), (1, 0, 0), 90).translate((0, 0, 0))
        sp1 = wp().sphere(30).translate((0, tl2 / 3, 0))
        sp2 = wp().sphere(30).translate((0, -tl2 / 3, 0))

        socket_y_offset = -35

        palm_cup = palm_cup.union(sp1).union(sp2)
        cut_box = wp().box(100, 150, 60).translate((0, 0, -5))
        palm_cup = palm_cup.cut(cut_box).translate((0, socket_y_offset / 2, -15))

        # ball = wp().sphere(15).translate((5, -20, 0))
        # return top.union(guard).union(palm_cup)
        top = top.union(palm_cup)  # .union(guard)
        # top = top.faces().edges(">X and <Y").fillet(8)
        # top = top.faces().edges(">Z").fillet(0.5)
        guard_base = make_guard(side_guard_width, side_guard_length, side_guard_height * 2)
        guard_cutter = make_guard(side_guard_width - 4, side_guard_length + 10, side_guard_height * 2)
        guard_cutter = guard_cutter.translate((0, 5, side_guard_height))
        # guard_cutter = guard_cutter.faces("|Z").edges().fillet(2)
        guard_base = guard_base.cut(guard_cutter)
        guard_base = guard_base.translate((0, -side_guard_length + 15, top_height))

        top = top.union(guard_base)

        socket_offset = 0
        socket_outer = wp().sphere(socket_radius + 1.5 + socket_tolerance).translate(
            (0, socket_y_offset, socket_offset + 3))
        # cutter2 = wp().box(socket_radius * 3, socket_radius * 3, 5).translate((0, 0, socket_radius + 3 + socket_tolerance))
        # socket_outer = socket_outer.cut(cutter2)
        socket_inner = wp().sphere(socket_radius + socket_tolerance).translate((0, socket_y_offset, socket_offset))
        cutter = wp().box(socket_radius * 3, socket_radius * 3, 20)
        flange_height = 7
        cutter = cutter.union(wp().box(6, socket_radius * 3, 22).translate((0, 0, flange_height)))
        cutter = cutter.union(wp().box(socket_radius * 3, 6, 22).translate((0, 0, flange_height)))
        # cutter = cutter.union(wp().box(4, socket_radius * 3, 20).rotate((0, 0, -1), (0, 0, 1), -45).translate((0, 0, flange_height)))
        # cutter = cutter.union(wp().box(4, socket_radius * 3, 20).translate((0, 0, flange_height)))
        cutter = cutter.translate((0, socket_y_offset, socket_offset - 15))

        # top = top.rotate((0, 1, 0), (0, -1, 0), -15)
        top = top.translate((0, 0, 3))
        top = top.union(socket_outer).cut(socket_inner).cut(cutter)

        # test_socket = socket_outer.cut(socket_inner).cut(cutter)
        # test_box_bottom = wp().box(20, 20, 4).translate((0, -35, socket_radius + 3.5))
        # test_socket = test_socket.union(test_box_bottom).rotate((-1, 0, 0), (1, 0, 0), 180)
        # top = top.faces("<Z").edges().fillet(0.5)
        # top = top.rotate((-1, 0, 0), (1, 0, 0), 10)
        top = top.translate((0, 0, height))
        return top.translate((-5, 0, 0))

    def make_bottom_holder():
        front_width = top_width / 2
        base_width = top_width
        base_len = top_len - 10
        bl2 = base_len / 2
        bw2 = base_width / 2
        fw2 = (base_width - front_width) / 2

        pts = [
            (-fw2, bl2),  # top left
            (fw2, bl2),  # top right
            (bw2, -bl2),  # mid right
            (-bw2, -bl2),  # bottom left
            (-fw2, bl2)  # top left
        ]

        # outline = wp().polyline(pts).close()
        outline = wp().circle(30).translate((-15, 0))
        base = outline.extrude(3)
        outline = wp().rect(60, 60)
        base = base.union(outline.extrude(3))
        outline = wp().circle(30).translate((15, 0))
        base = base.union(outline.extrude(3))

        # base = base.faces().edges("|Z").fillet(10)

        base = base.faces().edges("<Z").chamfer(1)
        base = base.faces().edges(">Z").chamfer(1)
        base = base.translate((0, 0, 0))

        # trunk = wp().box(15, 30, height).translate((0, -15, height / 2))
        # trunk = trunk.faces().edges("|Z").fillet(5)
        trunk = wp().cylinder(height, 7).translate((0, 0, height / 2))

        ball_join = (wp().sphere(socket_radius)
                     .union(wp().cylinder(30, 2.5).rotate((1, 0, 0), (-1, 0, 0), 90).translate((0, 0, -2)))
                     .union(wp().cylinder(30, 2.5).rotate((0, 1, 0), (0, -1, 0), 90).translate((0, 0, -2))))

        ball_join = ball_join.translate((0, 0, height))
        # return top.union(guard).union(palm_cup)
        # top = trunk.union(ball)
        return base.union(trunk).union(ball_join)

    # guard_base = make_guard(side_guard_width, side_guard_length, side_guard_height * 2)
    # guard_cutter = make_guard(side_guard_width - 4, side_guard_length + 10, side_guard_height * 2)
    # guard_cutter = guard_cutter.translate((0, 5, side_guard_height))
    # # guard_cutter = guard_cutter.faces("|Z").edges().fillet(2)
    # guard_base = guard_base.cut(guard_cutter)

    return make_top_base(), make_bottom_holder()


def puck_holder():
    main_puck = wp().cylinder(6.6, 41.1)

    cone = wp().union(cq.Solid.makeCone(radius1=60, radius2=45, height=8.1))

    cone = cone.cut(main_puck)
    return cone


def puck_plate():
    offset = 19.55
    border = 5
    border_half = border / 2
    width = offset * 5
    height = offset * 4

    # plate = box(width, height, 2)

    plate = wp().box(width, height,
                     1)  # .faces('>Z').rect(width, height).workplane(offset=2).rect(width / 2 + 5, height / 2 + 5).loft(combine=True)

    holes = [
        [offset, 0, 0],
        [0, offset, 0],
        [-offset, 0, 0],
        [0, -offset, 0]
    ]

    plate = plate.edges("|Z").fillet(25)
    plate = plate.edges(">Z").chamfer(0.7)
    plate = plate.faces(">Z").workplane().rect(38.1, 38.1, forConstruction=True).vertices().cboreHole(2.2, 3, .5, 5)
    return plate


def screw_mount():
    result = (
        cq.Workplane("XY")
        .circle(15)
        .workplane(offset=5.0)
        .circle(8)
        .loft(combine=True)
    )

    screw = cq.importers.importStep("./quarter_inch_screw.step").translate([0, 0, -10.5])

    return result.cut(screw)


def usb_c_mount():
    min_vert = 14.55
    max_vert = 16.2
    width = 5.5
    depth = 4.3
    wall_depth = 4

    walls = wp().box(width + wall_depth, 6 + wall_depth, max_vert + wall_depth)

    slot = wp().box(width, 6 + wall_depth, max_vert).translate((0, -depth + 1, 0))

    walls = walls.cut(slot)

    wedge = wp(orient="YZ").lineTo(0, ((max_vert - 0.2) / 2)).lineTo(depth, min_vert / 2).lineTo(depth,
                                                                                                 -min_vert / 2).lineTo(
        0, -(max_vert - 0.2) / 2).close().extrude(width)
    # wedge = wedge.translate((-(width / 2), -depth / 2, -depth / 2))
    wedge = wedge.translate((-(width / 2), 1, 0))
    walls = walls.cut(wedge)
    return walls


chair_top, chair_mount = hand_chair()

cq.exporters.export(threaded_cylinder(), "./threaded_cylinder.stl")
# show(chair_top.translate((0, 0, 15)).union(chair_mount))
# show(chair_mount)

# cq.exporters.export(chair_top, "./hand_chair_top.stl")
cq.exporters.export(chair_mount, "./hand_chair_mount.stl")
cq.exporters.export(chair_top, "./hand_chair_top.stl")

cq.exporters.export(chair_mount, "./hand_chair_mount.step")
cq.exporters.export(chair_top, "./hand_chair_top.step")
# cq.exporters.export(guard, "./guard.stl")
