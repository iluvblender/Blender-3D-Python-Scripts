import bpy
from mathutils import Vector

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

C = bpy.context
D = bpy.data

bb = lambda : tuple(
                    map(
                        lambda v: C.active_object.matrix_world.translation + v, 
                        map(
                            Vector, C.active_object.bound_box
                        )
                    )
              )

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


