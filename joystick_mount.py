from cq_shortcuts import *
from math import sin, cos, pi


def joystick_mount():
    bulb_radius = 150
    pcb_width = 38.1
    pcb_length = 25

    joystick_hole_radius = 7

    outer_sphere = wp().sphere(bulb_radius)
    inner_cut = wp().sphere(bulb_radius - 3)
    outer_sphere = outer_sphere.cut(inner_cut)

    top_cap = outer_sphere.cut(wp().box(300, 300, 300).translate((0, 0, -10)))

    pcb_mount = wp().box(pcb_width + 3, pcb_length + 3, 5).cut(wp().box(pcb_width, pcb_length, 5).translate((0, 0, -2))).translate((0, 0, 143))

    top_cap = top_cap.union(pcb_mount)

    post_cutter = wp().cylinder(300, joystick_hole_radius)
    top_cap = top_cap.cut(post_cutter)

    outer_cut = wp().cylinder(100, 80).cut(wp().cylinder(100, 22)).translate((0, 0, 140))
    top_cap = top_cap.cut(outer_cut)

    return top_cap.translate((0, 0, -150))


joy_mount = joystick_mount()

cq.exporters.export(joy_mount, "./joystick_mount.step")
cq.exporters.export(joy_mount, "./joystick_mount.stl")
