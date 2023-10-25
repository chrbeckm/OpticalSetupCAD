"""
Created: October 2022
Author: Christian Beckmann

Usage: Use as an import in scripts for complete setups as a database
    - Each function contains the code to build one optical element.
    - Each optical element has its optical axis at 100mm,
        if not stated otherwise.
    - Each optical element is facing in positiv x-axis.
    - The rotation center is at (0, 0), rotations are mathematically positive.
"""


import cadquery as cq

def place_cryostat(assy, file, x, y, angle, nr):
    if "cryo_large" not in globals():
        global cryo_large
        cryo_large = cq.importers.importStep("combined_files/Cryostat_large.step")
    assy.add(
        cryo_large,
        name=f"cryo_large-{nr}",
        loc=cq.Location(cq.Vector(x, 0, y), cq.Vector(0, 1, 0), angle),
    )
    file.write(f"\nCryo Large\t{nr}\t{x/25:.2f}\t{y/25:.2f}\t{x:.2f}\t{y:.2f}\t{angle:.3f}")


def place_lmr1m(assy, file, x, y, angle, nr):
    # 1" ø optics mount
    ### https://www.thorlabs.com/thorproduct.cfm?partnumber=LMR1/M
    if "lmr1m" not in globals():
        global lmr1m
        lmr1m = cq.importers.importStep("combined_files/LMR1_M.step")
    assy.add(
        lmr1m,
        name=f"lmr1m-{nr}",
        loc=cq.Location(cq.Vector(x, 0, y), cq.Vector(0, 1, 0), angle),
    )
    file.write(f"\nLMR1M\t{nr}\t{x/25:.2f}\t{y/25:.2f}\t{x:.2f}\t{y:.2f}\t{angle:.3f}")



