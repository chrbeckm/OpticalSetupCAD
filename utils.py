"""
Created: November 2022
Author: Christian Beckmann

See: https://cadquery.readthedocs.io/en/latest/assy.html#assembly-colors
    for full documentation of the available colors.

Usage: Use as a dumb file for all the "useful" functions
"""

import cadquery as cq
import numpy as np
import combined as cm


def calculate_angle(a1, b1, a2, b2):
    # a = x-coordinate
    # b = z-coordinate
    # 1 = first coordinate
    # 2 = second coordinate
    da = a2 - a1
    db = b2 - b1
    if da > 0:
        angle_ab = -np.rad2deg(np.arctan(db / da))
    elif da < 0:
        angle_ab = 180 - np.rad2deg(np.arctan(db / da))
    elif da == 0 and db > 0:
        angle_ab = -90
    elif da == 0 and db < 0:
        angle_ab = 90
    else:
        print("Wrong angle_ab in line")
        print(
            "Previous point:",
            a1,
            b1,
            a1 / 25,
            b1 / 25,
            sep="\t",
        )
        print(
            "Current point:",
            a2,
            b2,
            a2 / 25,
            b2 / 25,
            sep="\t",
        )
        angle_ab = 0

    while angle_ab < 0:
        angle_ab += 360
    while angle_ab > 360:
        angle_ab -= 360

    return angle_ab


def markers(assy, x_length, z_length, dx=0, dz=0):
    ### Just the hole markers
    x_points = np.arange(-x_length / 2, x_length / 2 + 1, 25)
    z_points = np.arange(-z_length / 2, z_length / 2 + 1, 25)
    point_list = []

    for x in x_points:
        for z in z_points:
            point_list.append((x, z))

    print("Nr. of holes:", len(point_list))

    markers = cq.Workplane("XZ").pushPoints(point_list).circle(3)

    assy.add(
        markers,
        name="markers",
        loc=cq.Location(cq.Vector(x_length / 2 + dx, 0, z_length / 2 + dz)),
    )


def table(assy, x_length, z_length, height=1, dx=0, dz=0):
    ### For full plate with holes
    x_points = np.arange(-x_length / 2, x_length / 2 + 1, 25)
    z_points = np.arange(-z_length / 2, z_length / 2 + 1, 25)
    point_list = []

    for x in x_points:
        for z in z_points:
            point_list.append((x, z))

    print("Nr. of holes:", len(point_list))

    table = (
        cq.Workplane("XZ")
        .rect(x_length, z_length)
        .extrude(height)
        .pushPoints(point_list)
        .rect(3, 3)
        .cutThruAll()
    )

    assy.add(
        table,
        name="table",
        loc=cq.Location(cq.Vector(x_length / 2 + dx, -height / 2, z_length / 2 + dz)),
    )


def line(assy, file, point_list, nr):
    nrofp = len(point_list)
    pl = []
    if len(point_list[0]) == 4:
        tup = (point_list[0][0] + point_list[0][2], point_list[0][1] + point_list[0][3])
        pl.append(tup)
    else:
        pl.append(point_list[0])
    if len(point_list[1]) == 4:
        tup = (point_list[1][0] + point_list[1][2], point_list[1][1] + point_list[1][3])
        pl.append(tup)
    else:
        pl.append(point_list[1])

    for i in range(1, nrofp - 1):
        if len(point_list[i + 1]) == 4:
            tup = (
                point_list[i + 1][0] + point_list[i + 1][2],
                point_list[i + 1][1] + point_list[i + 1][3],
            )
            pl.append(tup)
        else:
            pl.append(point_list[i + 1])

        x1, z1 = pl[i - 1]  # Point a
        x2, z2 = pl[i]  # Point b
        x3, z3 = pl[i + 1]  # Point c

        angle12 = calculate_angle(x1, z1, x2, z2)
        angle12in2 = angle12 - 180

        while angle12in2 < 0:
            angle12in2 += 360
        while angle12in2 > 360:
            angle12in2 -= 360

        angle23 = calculate_angle(x2, z2, x3, z3)

        if np.abs(angle23 - angle12in2) < 180:
            turning_angle = angle23 - (angle23 - angle12in2) / 2
            # print("Case1", angle12, angle12in2, angle23, turning_angle, sep="\t")
        elif angle23 - angle12in2 < 180:
            turning_angle = angle23 - (angle23 + 360 - angle12in2) / 2
            # print("Case2", angle12, angle12in2, angle23, turning_angle, sep="\t")
        elif angle23 - angle12in2 > 180:
            turning_angle = angle23 - (angle23 - angle12in2 - 360) / 2
            # print("Case3", angle12, angle12in2, angle23, turning_angle, sep="\t")
        # Own Mirror assembly needs to be defined
        # cm.place_mirror(assy, file, *pl[i], turning_angle, f"line-{nr}-{i}")


def beam(assy, point_list, nr, choosen_color, radius=2, circle=False):
    # See: https://cadquery.readthedocs.io/en/latest/assy.html#assembly-colors
    # for full documentation of the available colors
    overall_length = 0
    pl = []
    if len(point_list[0]) == 4:
        tup = (point_list[0][0] + point_list[0][2], point_list[0][1] + point_list[0][3])
        pl.append(tup)
    else:
        pl.append(point_list[0])
    for i in range(len(point_list) - 1):
        if len(point_list[i + 1]) == 4:
            tup = (
                point_list[i + 1][0] + point_list[i + 1][2],
                point_list[i + 1][1] + point_list[i + 1][3],
            )
            pl.append(tup)
        else:
            pl.append(point_list[i + 1])
        dx = pl[i + 1][0] - pl[i][0]
        dz = pl[i + 1][1] - pl[i][1]
        length = np.sqrt(dx ** 2 + dz ** 2)
        overall_length += length
        angle = calculate_angle(
            pl[i][0],
            pl[i][1],
            pl[i + 1][0],
            pl[i + 1][1],
        )
        if circle == False:
            beam_part = cq.Workplane("ZY").rect(radius * 2, radius * 2).extrude(-length)
        else:
            beam_part = cq.Workplane("ZY").circle(radius).extrude(-length)
        assy.add(
            beam_part,
            name=f"{nr}-{i}-{choosen_color}",
            loc=cq.Location(
                cq.Vector(pl[i][0], 100, pl[i][1]),
                cq.Vector(0, 1, 0),
                angle,
            ),
            color=cq.Color(choosen_color),
        )
    print(
        f"The length of beam {nr:<20}\tis {overall_length:7.2f};\t color {choosen_color}."
    )
    return overall_length


def text(assy, x, z, height, angle, text, nr, choosen_color, fontsize=10, depth=0):
    # See: https://cadquery.readthedocs.io/en/latest/assy.html#assembly-colors
    # for full documentation of the available colors
    t = cq.Workplane("ZX").text(text, fontsize, depth, halign="left", valign="bottom")
    assy.add(
        t,
        name=f"text_{text}_{nr}",
        loc=cq.Location(cq.Vector(x, height, z), cq.Vector(0, 1, 0), 180 + angle),
        color=cq.Color(choosen_color),
    )

def counter(assy,x_high, y_high, x_low=5, x_step=5, y_low=5, y_step=5):
    text(assy, *p(1.35, 0), 0, 90, "1", "x_0_1", "black", 20)
    text(assy, *p(1.35, y_high - 0.75), 0, 90, "1", "x_1_1", "black", 20)
    for i in np.arange(x_low, x_high, x_step):
        text(assy, *p(i + 0.35, 0), 0, 90, f"{i}", f"x_0_{i}", "black", 20)
        text(assy, *p(i + 0.35, y_high - 0.75), 0, 90, f"{i}", f"x_1_{i}", "black", 20)
    text(assy, *p(0, 1), 0, 180, "1", "z_0_1", "black", 20)
    text(assy, *p(x_high + 1.35, 1), 0, 180, "1", "z_1_1", "black", 20)
    for i in np.arange(y_low, y_high, y_step):
        text(assy, *p(0, i - 0.35), 0, 180, f"{i}", f"z_0_{i}", "black", 20)
        text(assy, *p(x_high + 1.35, i - 0.35), 0, 180, f"{i}", f"z_1_{i}", "black", 20)