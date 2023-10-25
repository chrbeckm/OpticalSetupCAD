# OpticalSetupCAD
Design your optical setup with python and the actual optical elements.

This library utilizes [CadQuery](https://cadquery.readthedocs.io/en/latest/intro.html). For visualization I use [CQ-Editor](https://github.com/CadQuery/CQ-editor) and [FreeCAD](https://www.freecad.org/).

## Workflow
Many suppliers of optical components offer `.step`-files for their products. These can be used to build the various components of your setup as 3D models.

In this example I will show it with the [RS3P4M](https://www.thorlabs.com/thorProduct.cfm?partNumber=RS3P4M) pedestal and [LMR1/M](https://www.thorlabs.com/thorproduct.cfm?partnumber=LMR1/M#ad-image-0) lens mount.
First download the `.step`-files and save them to the `object_files` directory.
Open `import_export.py` in _CQ-Editor_, import the files and place the objects fittingly together.
I aligned every component to a beam travelling the _x_-axis from positive to negative and the _x_-_z_-plane is the foundation.
The combo is then saved to the `combined_files` directory, your defintion can be saved to `defintions.py`.
Open `combinations.py` in the editor of your choice and add your combined file to it.

`utils.py` has some useful functions.
- `calculate_angle` is used internally
- `markers` places circles in the _x_-_z_-plane at 25mm distance, symbolising the holes in the table
- `table` does the same as `markers` but builds a plane and drills the holes
- `line` places mirror objects at the points in a given list, so you don't need to set each one per hand
- `beam` 
