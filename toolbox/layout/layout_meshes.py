import bpy

if not all(map(lambda obj: obj.type =='MESH', 
               bpy.context.selected_objects)):
    raise ValueError("You must select mesh objects only")

ao = bpy.context.active_object

other_objects = set(bpy.context.selected_objects) - set([ao])

gap = 0.1

offset = ao.dimensions.x/2.0

for obj in other_objects:
    adjust = obj.dimensions.x/2.0 + gap
    obj.location.x = offset + adjust
    offset = obj.location.x + adjust
