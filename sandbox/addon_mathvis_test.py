"""
# Usage

mod = bpy.data.texts['mathviz1.py'].as_module()
exec(mod.code)
loc = sum((bb0, bb4, bb7, bb3), Vector((0, 0, 0))) * 0.25
bpy.ops.object.empty_add(location=loc)
bpy.ops.object.empty_add(location=loc, 
                          rotation=mtx.decompose()[1].to_euler())
"""

import bpy
from mathutils import Vector


code = """
ao = bpy.context.active_object

mtx = ao.matrix_world

bbpts = map(Vector, ao.bound_box)

for index, point in enumerate(bbpts):
    exec("bb{0} = ao.matrix_world @ point".format(index), 
          globals(),
    )

del(point)
"""
