from cq_shortcuts import *
from math import sin, cos, pi
from build123d import *
from bd_warehouse.thread import IsoThread
from ocp_vscode import *
from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults

set_port(3939)

SEGMENTS = 48

def hand_chair():
    top_len = 80
    top_width = 60
    tl2 = top_len / 2
    tw2 = top_width / 2
    top_height = 10

    side_guard_width = top_width * 2 + 15
    side_guard_length = 50
    side_guard_height = top_height

    socket_radius = 12
    socket_tolerance = 0.05

    height = 32

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
        rotation = 25

        sg_width_2 = sg_width / 2

        side_offset = 20
        guard_right = wp().box(sg_width_2 + 12, sg_length, sg_height).translate((sg_width / 4, 0, 0))

        guard_left = wp().box(sg_width_2, sg_length - side_offset, sg_height).translate((-sg_width / 4, -side_offset / 2, 0))

        guard = guard_right.union(guard_left)

        cutter_right = rotate(wp().box(50, 200, 100).translate((sg_width_2, 0, 0)), (0, 30, -rotation)) # .rotate((0, 0, 1), (0, 0, -1), rotation)
        cutter_left = rotate(wp().box(50, 200, 100).translate((-sg_width_2, 0, 0)), (0, -30, rotation))
        return guard.cut(cutter_right).cut(cutter_left)
        # guard = guard.faces("<Z").edges().fillet(10)

        # return guard  # make_wall(side_guard_length, side_guard_width, side_guard_height, (0, 0, 0), (0, 0, 0))

    def make_top_base():

        cut_rad = 18  # (top_height + side_guard_height) / 2


        top = wp().box(top_width, top_len, top_height).translate((0, -20, top_height / 2))
        top = top.faces().edges("|Z").fillet(24)
        # top = top.faces().edges("<X and <Y").fillet(40)
        top = top.faces(">Z").edges().fillet(5)
        top = top.faces("<Z").edges().fillet(3)


        palm_cup = wp().cylinder(2 * (tl2 / 3), 30).rotate((-1, 0, 0), (1, 0, 0), 90).translate((0, 0, 0))
        sp1 = wp().sphere(30).translate((0, tl2 / 3, 0))
        sp2 = wp().sphere(30).translate((0, -tl2 / 3, 0))

        socket_y_offset = -35

        palm_cup = palm_cup.union(sp1).union(sp2)
        cut_box = wp().box(100, 150, 60).translate((0, 0, -5))
        palm_cup = palm_cup.cut(cut_box).translate((0, socket_y_offset / 2 - 5, -15))

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
        socket_offset = -2
        socket_outer = wp().sphere(socket_radius + 2 + socket_tolerance).translate(
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
        cutter = cutter.translate((0, socket_y_offset, socket_offset - 16))

        # top = top.rotate((0, 1, 0), (0, -1, 0), -15)
        
        top = top.translate((0, 0, 3))
        socket_inner = rotate(socket_inner, (-5, -10, 0)) # socket_inner.rotate((0, -1, 0), (0, 1, 0), -10)
        cutter = rotate(cutter, (-5, -10, 0))  #   cutter.rotate((0, -1, 0), (0, 1, 0), -10)
        top = top.union(socket_outer).cut(socket_inner).cut(cutter)

        # test_socket = socket_outer.cut(socket_inner).cut(cutter)
        # test_box_bottom = wp().box(20, 20, 4).translate((0, -35, socket_radius + 3.5))
        # test_socket = test_socket.union(test_box_bottom).rotate((-1, 0, 0), (1, 0, 0), 180)
        # top = top.faces("<Z").edges().fillet(0.5)
        # top = top.rotate((-1, 0, 0), (1, 0, 0), 10)
        top = top.translate((0, 0, height))
        return top.translate((-5, 0, 0))   
    
    def make_trunk():
        iso_external = IsoThread(
            major_diameter=13.2 * MM,
            pitch=1.8 * MM,
            length=height * MM * 0.9,
            external=True,
            end_finishes=("square", "square"),
            hand="right"
        )
        print(f"root_radius: {iso_external.root_radius}")
        external_core = Cylinder(
            iso_external.root_radius,
            height * MM,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        iso_external_screw = iso_external.fuse(external_core)

        return iso_external_screw
    
    def make_base_post():
        iso_internal = IsoThread(
            major_diameter=14 * MM,
            pitch=1.8 * MM,
            length=height * MM / 1.25,
            external=False,
            end_finishes=("chamfer", "fade"),
            hand="right",
        )
        with BuildPart() as iso_internal_shaft:
            with BuildSketch():
                Circle(iso_internal.major_diameter / 2 + 3)
                Circle(iso_internal.major_diameter / 2, mode=Mode.SUBTRACT)
            extrude(amount=iso_internal.length)
            
        return iso_internal.fuse(iso_internal_shaft.part)
        
    def make_nut():
        iso_internal = IsoThread(
            major_diameter=14 * MM,
            pitch=1.8 * MM,
            length=4.5 * MM,
            external=False,
            end_finishes=("chamfer", "fade"),
            hand="right",
        )
        
        with BuildPart() as iso_internal_nut:
            with BuildSketch():
                RegularPolygon(iso_internal.major_diameter * 0.7, 10)
                RectangleRounded(iso_internal.major_diameter + 8, 4, 1)
                RectangleRounded(4, iso_internal.major_diameter + 8, 1)
                Circle(iso_internal.major_diameter / 2, mode=Mode.SUBTRACT)
            extrude(amount=iso_internal.length)

        nut = iso_internal.fuse(iso_internal_nut.part)
        
        return nut
    
    def make_bottom_holder():
        front_width = top_width / 2
        base_width = top_width
        base_len = top_len - 10
        bl2 = base_len / 2
        bw2 = base_width / 2
        fw2 = (base_width - front_width) / 2

        # pts = [
        #     (-fw2, bl2),  # top left
        #     (fw2, bl2),  # top right
        #     (bw2, -bl2),  # mid right
        #     (-bw2, -bl2),  # bottom left
        #     (-fw2, bl2)  # top left
        # ]

        bottom = wp().circle(25).extrude(3)
        x = 0
        y = 0
        offset = 15
        for i in range(1, 3):
            outline = wp().rect(30, 60)
            angle = math.pi * 2 / 3 * i
            x = math.sin(angle) * offset
            y = math.cos(angle) * offset
           
            plate = outline.extrude(3)
            plate = plate.faces().edges("|Z").fillet(10)
            plate =  plate.rotate((0, 0, 1), (0, 0, -1), i * 120)
            plate = plate.translate((x, y, 0))
  
            bottom = bottom.union(plate)
            
        # outline = wp().polyline(pts).close()
        # outline = wp().rect(40, 40)
     
        # base = outline.extrude(3).translate((-15, 0, 0))
        # outline = wp().rect(30, 60)
        # base = base.union(outline.extrude(3))
        # outline = wp().circle(30)
        # base = base.union(outline.extrude(3).translate((15, 0, 0)))

        base = bottom
        # base = base.faces().edges("|Z").fillet(10)

        base = base.faces().edges("<Z").chamfer(1)
        base = base.faces().edges(">Z").chamfer(1)
        base = base.translate((0, 0, 0))

        # trunk = wp().box(15, 30, height).translate((0, -15, height / 2))
        # trunk = trunk.faces().edges("|Z").fillet(5)
        trunk_new = make_trunk()
                # external_core = Cylinder(
        #     iso_external.root_radius,
        #     iso_external.height * MM,
        #     align=(Align.CENTER, Align.CENTER, Align.MIN),
        # )
        # iso_external_screw = iso_external.fuse(external_core)
        core_radius = 5.6
        trunk = cq.Solid.makeCylinder(core_radius, height)  # trunk = cq.Solid.makeCylinder(6.188101183952089, height)
        # cq_obj = convert_shapes_to_cq(trunk_new)
        trunk.wrapped = trunk_new.solid().wrapped  # cq.Solid.makeCylinder(7, height).translate((0, 0, height / 2))
        cyl = wp().cylinder(height, core_radius).translate((0, 0, height / 2 - 1)).faces("<Z").edges().chamfer(0.5)
        trunk = cyl.union(trunk)
        shaft = make_base_post()
        nut = make_nut()

        cq_shaft = cq.Solid.makeCylinder(13, height)
        cq_shaft.wrapped = shaft.solid().wrapped
        
        
        # cq_obj = None
        # for obj in trunk_new.solids():
        #     new_obj = wp().cylinder(10, 5)
        #     if cq_obj is None:
        #         cq_obj = new_obj
        #         cq_obj.wrapped = obj.wrapped
        #     else:
        #         new_obj.wrapped = obj.wrapped
        #         cq_obj = cq_obj.union(new_obj)
                
        # trunk = cq_obj
        
        ball_join = (wp().sphere(socket_radius)
                     .union(wp().cylinder(30, 2.5).rotate((1, 0, 0), (-1, 0, 0), 90).translate((0, 0, -2)))
                     .union(wp().cylinder(30, 2.5).rotate((0, 1, 0), (0, -1, 0), 90).translate((0, 0, -2))))

        ball_join = ball_join.translate((0, 0, height))
        # return top.union(guard).union(palm_cup)
        # top = trunk.union(ball)
        ball_shaft = ball_join.union(trunk)
        base = base.union(cq_shaft)
        return base, ball_shaft, nut

    # guard_base = make_guard(side_guard_width, side_guard_length, side_guard_height * 2)
    # guard_cutter = make_guard(side_guard_width - 4, side_guard_length + 10, side_guard_height * 2)
    # guard_cutter = guard_cutter.translate((0, 5, side_guard_height))
    # # guard_cutter = guard_cutter.faces("|Z").edges().fillet(2)
    # guard_base = guard_base.cut(guard_cutter)
    top = make_top_base()
    base, ball_shaft, nut = make_bottom_holder()
    return top, base, ball_shaft, nut

chair_top, chair_mount, shaft, nut = hand_chair()

show(
    chair_top.translate((0, 0, 15)), 
    shaft,
    nut.translate((20, 20, 0)),
    chair_mount.translate((0, 0, -40))
)

# cq.exporters.export(threaded_cylinder(), "./threaded_cylinder.stl")
# show(chair_top.translate((0, 0, 15)).union(chair_mount))
# show(chair_mount)
export_stl(nut, "./nut.stl")
cq.exporters.export(shaft, "./shaft.stl")
cq.exporters.export(chair_mount, "./hand_chair_mount.stl")
cq.exporters.export(chair_top, "./hand_chair_top.stl")

cq.exporters.export(chair_mount, "./hand_chair_mount.step")
cq.exporters.export(chair_top, "./hand_chair_top.step")

cq.exporters.export(shaft, "./shaft.step")

