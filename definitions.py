"""
Created: October 2022
Author: Christian Beckmann

Usage: Predefine optical elements for setups
    - Each function contains the code to build one optical element.
    - Each optical element should be assembled in a way, that the optical axis is at 100mm,
        if not specified otherwise, e.g. 1.5" Beamsplitter right before the laser.
    - In combined usage with `import_export.py` and cadquery.
"""

import cadquery as cq
import numpy as np


def make_cryostat(assy):
    # code for a custom build cryostat
    xy_stage_0 = cq.Workplane("XZ").box(100, 100, 26)
    xy_stage_1 = cq.Workplane("XZ").box(32, 122, 18)
    xy_stage_2 = cq.Workplane("XZ").box(79, 32, 18)
    rot_stage = cq.Workplane("XZ").box(118, 118, 17.8)
    cryo = cq.Workplane("XZ").circle(75).extrude(100 - 26 - 17.8)
    assy.add(
        xy_stage_0,
        name="cryo_xy_0",
        loc=cq.Location(
            cq.Vector(0, 13, 0),
        ),
    )
    assy.add(
        xy_stage_1,
        name="cryo_xy_1",
        loc=cq.Location(
            cq.Vector(66, 13, -11),
        ),
    )
    assy.add(
        xy_stage_2,
        name="cryo_xy_2",
        loc=cq.Location(
            cq.Vector(-79 / 2, 13, -66),
        ),
    )
    assy.add(
        rot_stage,
        name="cryo_rotation",
        loc=cq.Location(
            cq.Vector(0, 26 + 17.8 / 2, 0),
        ),
    )
    assy.add(
        cryo,
        name="cryo",
        loc=cq.Location(
            cq.Vector(0, 100, 0),
        ),
    )


def make_lmr1m(assy, x, y):
    angle = 90
    rs3p4m = cq.importers.importStep("object_files/RS3P4M.step")
    lmr1 = cq.importers.importStep("object_files/LMR1_M.step")
    assy.add(
        rs3p4m,
        name=f"pedestal-lmr1",
        loc=cq.Location(cq.Vector(0 + x, 37.5, 0 + y)),
    )
    # recorrect the mount, as the axis is not at the sinkhole
    # np uses radiant
    alpha_0 = angle * np.pi / 180 + np.arctan(1.75 / 9.53)
    axiscenterlength = np.sqrt(9.53 ** 2 + 1.75 ** 2)
    px = x + np.cos(alpha_0) * axiscenterlength
    py = y - np.sin(alpha_0) * axiscenterlength
    assy.add(
        lmr1,
        name=f"lmr1",
        loc=cq.Location(cq.Vector(px, 75 + 14, py), cq.Vector(0, 1, 0), angle),
    )