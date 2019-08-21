import bpy
from mathutils import Vector

objects = bpy.data.collections['Primitives'].objects

offset = Vector(objects[0].bound_box[4]).x

for obj in objects[1:]:
    obj.location.x = offset + abs(obj.bound_box[0][0])
    offset = obj.location.x + abs(obj.bound_box[4][0])
