import operator

import bpy
from mathutils import Vector


# Bounding box axes

bbxmin = operator.itemgetter(0)
bbxmax = operator.itemgetter(4)

bbymin = operator.itemgetter(4)
bbymax = operator.itemgetter(7)
 
bbzmin = operator.itemgetter(7)
bbzmax = operator.itemgetter(6)

# Extract the x/y/z coordinate from a point

xcoord = operator.itemgetter(0)
ycoord = operator.itemgetter(1)
zcoord = operator.itemgetter(2)


def get_bbox(ob):
    bound_box = ob.bound_box
    translation = ob.matrix_world.translation
 
    return tuple(map(lambda v:  translation + v, 
                    map(Vector, ob.bound_box)
                )
            )    


def get_axis_extent(axis, extent, coords):
    return extent(map(axis, coords))


def get_combined_bounding_boxes(objects):
    bboxes = tuple(map(get_bbox, objects))

    coords = tuple(map(bbxmin, bboxes))
    min_x = get_axis_extent(xcoord, min, coords)
    
    coords = tuple(map(bbxmax, bboxes))
    max_x = get_axis_extent(xcoord, max, coords)
    
    coords = tuple(map(bbymin, bboxes))
    min_y = get_axis_extent(ycoord, min, coords)

    coords = tuple(map(bbymax, bboxes))
    max_y = get_axis_extent(ycoord, max, coords)

    coords = tuple(map(bbzmin, bboxes))
    min_z = get_axis_extent(zcoord, min, coords)
 
    coords = tuple(map(bbzmax, bboxes))
    max_z = get_axis_extent(zcoord, max, coords)
    
    bbc_0 = Vector((min_x, min_y, min_z))
    bbc_1 = Vector((min_x, min_y, max_z))
    bbc_2 = Vector((min_x, max_y, max_z))
    bbc_3 = Vector((min_x, max_y, min_z))
    bbc_4 = Vector((max_x, min_y, min_z))
    bbc_5 = Vector((max_x, min_y, max_z))
    bbc_6 = Vector((max_x, max_y, max_z))
    bbc_7 = Vector((max_x, max_y, min_z))

    return bbc_0, bbc_1, bbc_2, bbc_3, bbc_4, bbc_5, bbc_6, bbc_7    


"""
bb = D.texts['bb.py'].as_module()
objects = C.selected_objects
bc_0, bbc_1, bbc_2, bbc_3, bbc_4, bbc_5, bbc_6, bbc_7 = bb.get_combined_bounding_boxes(objects)
"""

## Version 2
"""
objects = C.seelcted_objects
bboxes = tuple(map(bb.get_bbox, objects))
>> bboxes[0]
(Vector((-1.0, -1.0, 2.0)), Vector((-1.0, -1.0, 4.0)), Vector((-1.0, 1.0, 4.0)), Vector((-1.0, 1.0, 2.0)), Vector((1.0, -1.0, 2.0)), Vector((1.0, -1.0, 4.0)), Vector((1.0, 1.0, 4.0)), Vector((1.0, 1.0, 2.0)))

>>> bboxes[1]
(Vector((-1.0, -1.0, 0.0)), Vector((-1.0, -1.0, 2.0)), Vector((-1.0, 1.0, 2.0)), Vector((-1.0, 1.0, 0.0)), Vector((1.0, -1.0, 0.0)), Vector((1.0, -1.0, 2.0)), Vector((1.0, 1.0, 2.0)), Vector((1.0, 1.0, 0.0)))

>>> coords = tuple(map(bb.bbxmin, bboxes))
(Vector((-1.0, -1.0, 2.0)), Vector((-1.0, -1.0, 0.0)))

>>> min_x = bb.get_axis_extent(bb.xcoord, min, coords)


>>> coords = tuple(map(bb.bbxmax, bboxes))
>>> max_x = bb.get_axis_extent(bb.xcoord, max, coords)

>> coords = tuple(map(bb.bbymin, bboxes))
>>> min_y = bb.get_axis_extent(bb.ycoord, min, coords)

>>> coords = tuple(map(bb.bbymax, bboxes))
>>> max_y = bb.get_axis_extent(bb.ycoord, max, coords)

>> coords = tuple(map(bb.bbzmin, bboxes))
>>> min_z = bb.get_axis_extent(bb.zcoord, min, coords)
 
>>> coords = tuple(map(bb.bbzmax, bboxes))
>>> max_z = bb.get_axis_extent(bb.zcoord, max, coords)

>>> bbc_0 = Vector((min_x, min_y, min_z))
>>> bbc_1 = Vector((min_x, min_y, max_z))
>>> bbc_2 = Vector((min_x, max_y, max_z))
>>> bbc_3 = Vector((min_x, max_y, min_z))
>>> bbc_4 = Vector((max_x, min_y, min_z))
>>> bbc_5 = Vector((max_x, min_y, max_z))
>>> bbc_6 = Vector((max_x, max_y, max_z))
>>> bbc_7 = Vector((max_x, max_y, min_z))

"""



## Version 1
"""
bb = lambda : tuple(
                    map(
                        lambda v: C.active_object.matrix_world.translation + v, 
                        map(
                            Vector, C.active_object.bound_box
                        )
                    )
              )

# Load the bounding box module
bb = D.texts['bb.py'].as_module()

# Draw the coordinates of the boinding box for the first selected objects
bb1_0, bb1_1, bb1_2, bb1_3, bb1_4, bb1_5, bb1_6, bb1_7 = bb.bb()

# Draw the coordinates of the boinding box for the second selected objects
bb2_0, bb2_1, bb2_2, bb2_3, bb2_4, bb2_5, bb2_6, bb2_7 = bb.bb()

## X dimension calculations
min_x = min(map(lambda v: v.x, (bb1_0, bb2_0)))
max_x = max(map(lambda v: v.x, (bb1_4, bb2_4)))

## Y dimension calculations
min_y = min(map(lambda v: v.y, (bb1_4, bb2_4)))
max_y = max(map(lambda v: v.y, (bb1_7, bb2_7)))

## Z dimension calculations
min_z = min(map(lambda v: v.z, (bb1_7, bb2_7)))
max_z = max(map(lambda v: v.z, (bb1_6, bb2_6)))

## Construct the combined bounding box using the min/max x/y/z coordinates

bbc_0 = Vector((min_x, min_y, min_z))
bbc_1 = Vector((min_x, min_y, max_z))
bbc_2 = Vector((min_x, max_y, max_z))
bbc_3 = Vector((min_x, max_y, min_z))
bbc_4 = Vector((max_x, min_y, min_z))
bbc_5 = Vector((max_x, min_y, max_z))
bbc_6 = Vector((max_x, max_y, max_z))
bbc_7 = Vector((max_x, max_y, min_z))
"""

"""
# min/max on each-axes
X: 
    min(bb1[0].x, bb2[0].x)
    max(bb1[4].x, bb2[4].x)

Y:
    min(bb1[4].y, bb2[4].y)
    max(bb1[7].y, bb2[7].y)

Z:
    min(bb1[7].z, bb2[7].z)
    min(bb1[6].z, bb2[6].z)
"""
