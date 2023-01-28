from cq_shortcuts import *

reset_holder = False

# connector_width = 9.3             # adjustable
# connector_height = 4.5             # kinda adjustable

CONNECTORS = {
    "USB-C": {
        "w": 4,
        "h": 10
    },
    "MICRO-USB": {
        "w": 10,
        "h": 4
    }
}


SERIAL = {
    "TRRS": {
        "w": 6.2,
        "l": 12.5,
        "h": 9,
        "shape": {
            "type": "circle",
            "r": 2.55
        }
    },
    "USB-C": {
        "w": 6.2,
        "l": 12.5,
        "h": 14,
        "shape": {
            "type": "rounded",
            "w": 4,
            "h": 10
        }
    }
}

CONTROLLERS = {
    "ELITE_C": {
        "w": 18.7,
        "l": 33.4,
        "h": 2,
        "side_cut": 6,
        "connector": "USB-C"
    },
    "PRO_MICRO": {
        "w": 18.7,
        "l": 33.4,
        "h": 1.5,
        "side_cut": 6,
        "connector": "MICRO-USB"
    },
    "KB_2040": {
        "w": 18.7,
        "l": 33.4,
        "h": 2,
        "side_cut": 6,
        "connector": "USB-C"
    },
    "BLACKPILL": {
        "w": 26.6,
        "l": 58.5,
        "h": 2,
        "side_cut": 6,
        "connector": "MICRO-USB"
    },
    "PI_PICO": {
        "w": 22,
        "l": 53,
        "h": 2,
        "side_cut": 6,
        "connector": "MICRO-USB"
    },

}

WALL_THICKNESS = 3
OUTER_FLANGE_THICKNESS = WALL_THICKNESS / 2
OUTER_FLANGE_LIP = 2

MIN_WIDTH = 30.6
MAX_WIDTH = 40
MIN_HEIGHT = 8
MAX_HEIGHT = 14

controller_name = "PI_PICO"
controller = CONTROLLERS[controller_name]
connector = CONNECTORS[controller["connector"]]

serial_name = "TRRS"
serial = SERIAL[serial_name]

test_width = min(max(serial['w'] + controller['w'] + 4, MIN_WIDTH), MAX_WIDTH)
test_height = min(max(serial['h'] + 2,  controller['h'] + 2), MAX_HEIGHT)

length = controller['l'] + 5

holder_border = 1.5   # kinda adjustable
holder_width = test_width + (2 * holder_border)     # kinda adjustable
holder_length = length + holder_border   # kinda adjustable
holder_height = test_height  # 15 if reset_holder else 8.4        # kinda adjustable

print(f"Holder width: {holder_width}, length: {holder_length}, height: {holder_height}")

#* this combination of controller and usb_c dimensions
# friction fits both generations of elite-c controllers
controller_width = controller['w']  # 18.7      # kinda adjustable
controller_length = controller['l']  # 33.4      # mostly adjustable
controller_side_cut = controller['side_cut']  # 6  # adjustable

connector_width = connector['w']                # adjustable
connector_height = connector['h']               # kinda adjustable

trrs_x = 6.2              # mostly adjustable
trrs_y = 12.5             # kinda adjustable
trrs_r = 2.55             # adjustable

holder_center_x = holder_width / 2
holder_center_y = holder_length / 2
holder_center_z = holder_height / 2

holder_notch_xy = holder_border
holder_notch_down = holder_border * holder_notch_xy
holder_notch_half = holder_notch_xy / 2

holder_edge = 2


def notch():
    return box(holder_notch_xy, holder_notch_xy, 99)


def circuit_board_slots():
    return box(controller_side_cut, controller_length, 99)


def basic_shape():
    controller_x = holder_center_x - holder_border - (controller_width / 2)
    serial_x = -holder_center_x + holder_border + (serial["w"] / 2)
    controller_y = holder_center_y - (holder_length - controller_length) / 2
    serial_y = holder_center_y - (holder_length - serial["l"]) / 2

    base = box(holder_width, holder_length, holder_height).translate([0, (holder_length / 2), holder_height / 2])
    taper = rotate_around_x(box(holder_width + 6, holder_length + 6, holder_height + 2).translate([0, 0, 2.5 + holder_height / 2]), 8)
    serial_box_x = (holder_width / 2) - (serial["w"] / 2)
    serial_box_y = (holder_length / 2) - (serial["l"] / 2)

    serial_box = box(serial["w"], serial["l"], holder_height).translate([serial_x, serial_y, holder_height / 2])
    behind_serial_cut = box(serial["w"] + 2, holder_length - serial["l"], 20).translate([-serial_box_x, -serial["l"], 0])

    controller_box = box(controller_width, controller_length, holder_height).translate([controller_x, controller_y, holder_height / 2])
    return base.cut(controller_box).cut(serial_box)
    # return base.cut(taper).cut(serial_box).cut(behind_serial_cut).cut(controller_box)


# def basic_shape():
#     base = box(holder_width, holder_length, holder_height)
#     taper = rotate_around_x(box(holder_width + 6, holder_length + 6, holder_height + 2).translate([0, 0, 2.5 + holder_height / 2]), 8)
#     serial_box_x = (holder_width / 2) - (serial["w"] / 2)
#     serial_box_y = (holder_length / 2) - (serial["l"] / 2)
#
#     serial_box = box(serial["w"], serial["l"], holder_height).translate([2 - serial_box_x, -4 + serial_box_y, 1])
#     behind_serial_cut = box(serial["w"] + 2, holder_length - serial["l"], 20).translate([-serial_box_x, -serial["l"], 0])
#
#     controller_box = box(controller_width, controller_length, holder_height).translate([-2 + holder_width / 2 - controller_width / 2, 0, 1])
#     return base.cut(taper).cut(serial_box).cut(behind_serial_cut).cut(controller_box)

# def basic_shape():
#     left_cut_x = 2 * usb_holder_border
#     left_cut_y = 3 * usb_holder_border
#
#     bottom_cut_x = (left_cut_x + trrs_x)
#     bottom_cut_y = (left_cut_x + trrs_x)
#
#     cut1_x = (usb_holder_center_x - usb_holder_border)
#     cut1_y = (usb_holder_center_y - (usb_holder_center_y - left_cut_y / 2))
#
#     cut2_x = (usb_holder_center_x - (bottom_cut_x / 2))
#     # cut2_y = (usb_holder_center_y - (- usb_holder_center_y(16.6 / 2)))
#     top_cut_adjust = 1.75 * usb_holder_border if reset_holder is not None else usb_holder_border
#
#     base = box(holder_width, holder_length, holder_height)
#     to_cut_1 = box(left_cut_x, (holder_length - left_cut_y), 99).translate((-cut1_x, -cut1_y, 0))
#     to_cut_2 = box(bottom_cut_x, (holder_length - (controller_length / 2)), 99).translate((-cut2_x, -(serial['l'] - 4), 0))
#     to_cut_3 = box(holder_width, holder_length, holder_height).translate((0, -(usb_holder_border * 3), (holder_height / top_cut_adjust)))
#     to_cut_3 = rotate_around_x(to_cut_3, 8)
#     notch_x = (usb_holder_center_x - usb_holder_notch_half)
#     notch_y = (usb_holder_center_y - usb_holder_notch_down)
#     base = base.cut(to_cut_1.union(to_cut_2) ) # .union(to_cut_3))
#
#     return base.cut(notch().translate((-notch_x, notch_y, 0)).union(notch().translate((notch_x, notch_y, 0))))


def trrs_cutouts():
    trrs_floor = 1
    trrs_square_cutout_height = 12
    trrs_square_cutout_height_offset = trrs_floor - holder_center_z + trrs_square_cutout_height / 2
    trrs = box(trrs_x, trrs_y, trrs_square_cutout_height).translate((-9.2, 11.65, trrs_square_cutout_height_offset))
    trrsAngle_z_adjust = 0.5 if not reset_holder else 4
    trrsAngle_z_factor = 0.5 if not reset_holder else 1

    trrs_1 = rotate_around_x(box(trrs_x, trrs_y, holder_height * trrsAngle_z_factor), -72).translate((-9.2, 11.65 - (trrs_y / 3), trrsAngle_z_adjust * holder_border))

    trrs = trrs.union(trrs_1)

    trrs_y_offset = (holder_center_y - (holder_border / 2) + 0.01)
    trrs_z_offset = (holder_center_z - (trrs_floor + trrs_r))

    trrs_2 = rotate_around_x(wp().cylinder(holder_border * 2, trrs_r), 90).translate((-9.1, trrs_y_offset, -trrs_z_offset))

    return trrs.union(trrs_2)


def reset_cutout():
    reset_xz = 7.1
    reset_y = 4.5
    reset_floor = holder_height / 1.5
    reset_r = 1.75

    reset_x_offset = holder_center_x - controller_width / 2 - holder_border
    reset_y_offset = holder_center_y - controller_length - holder_border
    reset_z_offset = holder_center_z - (reset_floor + reset_r)

    return box(reset_xz, reset_y, reset_xz).translate((reset_x_offset, -reset_y_offset, -reset_z_offset))\
        .union(rotate_around_x(wp().cylinder(99, reset_r), 90).translate((reset_x_offset, 0, -reset_z_offset)))


def usb_port_cutout():
    usbPortCenter = ((holder_center_x - (controller_width / 2)) - holder_border)
    usbPortCenterCut = abs(connector_width - connector_height)
    usbPortSideOffset = usbPortCenterCut / 2
    usbPortCenterCutLength = 35

    cutout = rotate_around_x(wp().cylinder(usbPortCenterCutLength, connector_height / 2), 90)\
        .translate((usbPortCenter - usbPortSideOffset, 0, 0))

    cutout = cutout.union(box(usbPortCenterCut, usbPortCenterCutLength, connector_height).translate((usbPortCenter, 0, 0)))\
        .union(rotate_around_x(wp().cylinder(usbPortCenterCutLength, connector_height / 2), 90).translate((usbPortCenter + usbPortSideOffset, 0, 0)))

    return cutout


def usb_recess_cutout():
    usb_c_cover_plate = holder_border
    recess_y = (holder_length - controller_length - holder_border - usb_c_cover_plate)
    recess_z = 8

    cutout = rotate_around_x(wp().cylinder(recess_y, 3.25), 90)
    cutout = cutout.union(box(12.5, recess_y, recess_z).translate((holder_center_x - (controller_width / 2), 0, 0)))
    cutout = cutout.union(rotate_around_x(wp().cylinder(recess_y, 3.25), 90).translate((connector_width, 0, 0)))

    return cutout.translate((0, holder_center_y - (recess_y / 2) + 0.01, 0))


def elite_c():
    x_offset = ((holder_center_x - (controller_width / 2)) - holder_border)
    y_offset = (-(holder_center_y - (controller_length / 2)) + holder_border)
    z_offset = holder_border

    left_cut_x  = ((holder_center_x - (controller_width / 2)) - ((controller_width / 2) - (controller_side_cut / 2)) - holder_border)
    right_cut_x = ((holder_center_x - (controller_width / 2)) + ((controller_width / 2) - (controller_side_cut / 2)) - holder_border)

    usbPort_z_adjust = -3.6 if reset_holder else -0.3

    ec = box(controller_width, controller_length, holder_height).translate((x_offset, y_offset, z_offset))
    ec = ec.union(circuit_board_slots().translate((left_cut_x, y_offset, 0)))
    ec = ec.union(circuit_board_slots().translate((right_cut_x, y_offset, 0)))
    ec = ec.union(usb_port_cutout().union(usb_recess_cutout()).translate((0, 0, usbPort_z_adjust)))

    return ec


def usb_holder():
    shape = basic_shape()  # .translate((0, -(usb_holder_y / 2), usb_holder_z / 2))
    # shape = shape.cut(trrs_cutouts()).cut(elite_c()).cut(reset_cutout())
    print("Done")
    return shape


show_object(usb_holder())
