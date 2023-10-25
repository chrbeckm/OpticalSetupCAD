"""
Created: November 2022
Author: Christian Beckmann

Usage: Simple schematic
"""
import cadquery as cq
from os import getcwd as osgetcwd
from sys import path as pins

pins.insert(0, osgetcwd())

import combined as cm
import utils as ut


def h(x):
    return 25 * x


def p(x, y):
    return (h(x), h(y))


assy = cq.Assembly()
f = open("full_schemes/showcase_positions.txt", "w")
f.write("Optic\tName\tx/hole\tz/hole\tx/mm\tz/mm")

ut.markers(assy, h(5), h(3), h(1), h(1))

cryostat = cq.Workplane().box(40, 40, 40)
assy.add(cryostat, name="cryostat", loc=cq.Location(cq.Vector(h(-3), 100, h(9))))

cm.place_cryostat(assy, f, *p(-3, 2), 40, "cryostat_large")

beampath = [p(0, 0), p(0, 4), p(-5, 4), p(-5, 10)]
ut.beam(assy, beampath, 0, "red", radius=5, circle=True)

ut.text(assy, h(-5.2), h(-3), 100, -180, "Some text", 0, "black", 24)

f.close()
assy.save("full_schemes/showcase.step")
