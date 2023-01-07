from cq_shortcuts import *

reset_holder = True

usb_holder_x = 30.6       # kinda adjustable
usb_holder_y = 38.8       # kinda adjustable
usb_holder_z = 15 if reset_holder else 8.4        # kinda adjustable

usb_holder_border = 1.5   # kinda adjustable

#* this combination of controller and usb_c dimensions
# friction fits both generations of elite-c controllers
usb_elite_c_x = 18.7      # kinda adjustable
usb_elite_c_y = 33.4      # mostly adjustable
usb_elite_c_side_cut = 6  # adjustable

usb_c_x = 9.3             # adjustable
usb_c_z = 4.5             # kinda adjustable

trrs_x = 6.2              # mostly adjustable
trrs_y = 12.5             # kinda adjustable
trrs_r = 2.55             # adjustable

usb_holder_center_x = usb_holder_x / 2
usb_holder_center_y = usb_holder_y / 2
usb_holder_center_z = usb_holder_z / 2

usb_holder_notch_xy = usb_holder_border
usb_holder_notch_down = usb_holder_border * usb_holder_notch_xy
usb_holder_notch_half = usb_holder_notch_xy / 2


def notch():
    return box(usb_holder_notch_xy, usb_holder_notch_xy, 99)


def circuit_board_slots():
    return box(usb_elite_c_side_cut, usb_elite_c_y, 99)


def basic_shape():
    left_cut_x = 2 * usb_holder_border
    left_cut_y = 3 * usb_holder_border

    bottom_cut_x = (left_cut_x + trrs_x)
    bottom_cut_y = (left_cut_x + trrs_x)

    cut1_x = (usb_holder_center_x - usb_holder_border)
    cut1_y = (usb_holder_center_y - (usb_holder_center_y - left_cut_y / 2))

    cut2_x = (usb_holder_center_x - (bottom_cut_x / 2))
    # cut2_y = (usb_holder_center_y - (- usb_holder_center_y(16.6 / 2)))
    top_cut_adjust = 1.75 * usb_holder_border if reset_holder is not None else usb_holder_border

    base = box(usb_holder_x, usb_holder_y, usb_holder_z)
    to_cut_1 = box(left_cut_x, (usb_holder_y - left_cut_y), 99).translate((-cut1_x, -cut1_y, 0))
    to_cut_2 = box(bottom_cut_x, (usb_holder_y - 16.6), 99).translate((-cut2_x, -8.3, 0))
    to_cut_3 = box(usb_holder_x, usb_holder_y, usb_holder_z).translate((0, -(usb_holder_border * 3), (usb_holder_z / top_cut_adjust)))
    to_cut_3 = rotate_around_x(to_cut_3, 8)
    notch_x = (usb_holder_center_x - usb_holder_notch_half)
    notch_y = (usb_holder_center_y - usb_holder_notch_down)
    base = base.cut(to_cut_1.union(to_cut_2).union(to_cut_3))

    return base.cut(notch().translate((-notch_x, notch_y, 0)).union(notch().translate((notch_x, notch_y, 0))))


def trrs_cutouts():
    trrs_floor = 1
    trrs_square_cutout_height = 12
    trrs_square_cutout_height_offset = trrs_floor - usb_holder_center_z + trrs_square_cutout_height/2
    trrs = box(trrs_x, trrs_y, trrs_square_cutout_height).translate((-9.2, 11.65, trrs_square_cutout_height_offset))
    trrsAngle_z_adjust = 0.5 if not reset_holder else 4
    trrsAngle_z_factor = 0.5 if not reset_holder else 1

    trrs_1 = rotate_around_x(box(trrs_x, trrs_y, usb_holder_z * trrsAngle_z_factor), -72).translate((-9.2, 11.65 - (trrs_y / 3), trrsAngle_z_adjust * usb_holder_border))

    trrs = trrs.union(trrs_1)

    trrs_y_offset = (usb_holder_center_y - (usb_holder_border / 2) + 0.01)
    trrs_z_offset = (usb_holder_center_z - (trrs_floor + trrs_r))

    trrs_2 = rotate_around_x(wp().cylinder(usb_holder_border * 2, trrs_r), 90).translate((-9.1, trrs_y_offset, -trrs_z_offset))

    return trrs.union(trrs_2)


def reset_cutout():
    reset_xz = 7.1
    reset_y = 4.5
    reset_floor = usb_holder_z / 1.5
    reset_r = 1.75

    reset_x_offset = usb_holder_center_x - usb_elite_c_x / 2 - usb_holder_border
    reset_y_offset = usb_holder_center_y - usb_elite_c_y - usb_holder_border
    reset_z_offset = usb_holder_center_z - (reset_floor + reset_r)

    return box(reset_xz, reset_y, reset_xz).translate((reset_x_offset, -reset_y_offset, -reset_z_offset))\
        .union(rotate_around_x(wp().cylinder(99, reset_r), 90).translate((reset_x_offset, 0, -reset_z_offset)))


def usb_port_cutout():
    usbPortCenter = ((usb_holder_center_x - (usb_elite_c_x/2)) - usb_holder_border)
    usbPortCenterCut = (usb_c_x - usb_c_z)
    usbPortSideOffset = usbPortCenterCut / 2
    usbPortCenterCutLength = 35

    cutout = rotate_around_x(wp().cylinder(usbPortCenterCutLength, usb_c_z / 2), 90)\
        .translate((usbPortCenter - usbPortSideOffset, 0, 0))

    cutout = cutout.union(box(usbPortCenterCut, usbPortCenterCutLength, usb_c_z).translate((usbPortCenter, 0, 0)))\
        .union(rotate_around_x(wp().cylinder(usbPortCenterCutLength, usb_c_z / 2), 90).translate((usbPortCenter + usbPortSideOffset, 0, 0)))

    return cutout


def usb_recess_cutout():
    usb_c_cover_plate = usb_holder_border
    recess_y = (usb_holder_y - usb_elite_c_y - usb_holder_border - usb_c_cover_plate)
    recess_z = 8

    cutout = rotate_around_x(wp().cylinder(recess_y, 3.25), 90)
    cutout = cutout.union(box(12.5, recess_y, recess_z).translate((usb_holder_center_x - (usb_elite_c_x / 2), 0, 0)))
    cutout = cutout.union(rotate_around_x(wp().cylinder(recess_y, 3.25), 90).translate((usb_c_x, 0, 0)))

    return cutout.translate((0, usb_holder_center_y - (recess_y / 2) + 0.01, 0))


def elite_c():
    x_offset = ( (usb_holder_center_x - (usb_elite_c_x / 2)) - usb_holder_border)
    y_offset = (-(usb_holder_center_y - (usb_elite_c_y / 2)) + usb_holder_border)
    z_offset = usb_holder_border

    left_cut_x  = ((usb_holder_center_x - (usb_elite_c_x / 2)) - ((usb_elite_c_x / 2) - (usb_elite_c_side_cut / 2)) - usb_holder_border)
    right_cut_x = ((usb_holder_center_x - (usb_elite_c_x / 2)) + ((usb_elite_c_x / 2) - (usb_elite_c_side_cut / 2)) - usb_holder_border)

    usbPort_z_adjust = -3.6 if reset_holder else -0.3

    ec = box(usb_elite_c_x, usb_elite_c_y, usb_holder_z).translate((x_offset, y_offset, z_offset))
    ec = ec.union(circuit_board_slots().translate((left_cut_x, y_offset, 0)))
    ec = ec.union(circuit_board_slots().translate((right_cut_x, y_offset, 0)))
    ec = ec.union(usb_port_cutout().union(usb_recess_cutout()).translate((0, 0, usbPort_z_adjust)))

    return ec


def usb_holder():
    shape = basic_shape()  # .translate((0, -(usb_holder_y / 2), usb_holder_z / 2))
    shape = shape.cut(trrs_cutouts()).cut(elite_c()).cut(reset_cutout())
    print("Done")
    return shape


show_object(usb_holder())
