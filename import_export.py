"""
Created: October 2022
Author: Christian Beckmann

Usage: Predefine optical elements for setups
    - Use together with `definitions.py`.
    - The circle can be used to test the height of the optical axis.
    - Comment out when saving the assembly to a file.
    - Reduce time by not saving and importing the assembly (lines 29-31)
"""

import cadquery as cq
import numpy as np

from definitions import *

depth = 10
circle = cq.Workplane("YZ").circle(12.5).extrude(depth * 2)

assy = cq.Assembly()
### Do not place the circle if you are saving the assembly
# assy.add(circle, name="a", loc=cq.Location(cq.Vector(-depth, 100.4, 0)), color=cq.Color("red"))

object_file_name = "Cryostat_Large"
make_cryostat(assy)

### Saving the assembly and placing it at an distance and angle to check the file.
### Comment out if you are testing the assembly first.
assy.save(f"combined_files/{object_file_name}.step")
test = cq.importers.importStep(f"combined_files/{object_file_name}.step")
assy.add(test, name="test object", loc=cq.Location(cq.Vector(0, 0, -300), cq.Vector(0, 1, 0), 30))

### Show the object in `cq-editor`
show_object(assy)
