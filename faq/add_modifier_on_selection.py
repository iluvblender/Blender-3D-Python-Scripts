import bpy

selected_objects = bpy.context.selected_objects

for item in selected_objects:
    bpy.ops.object.select_all(action='DESELECT')
    
    bpy.context.view_layer.objects.active = item
    item.select_set(True)
    
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 2
