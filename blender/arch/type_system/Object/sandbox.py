ao = bpy.context.active_object
bbox = tuple(map(Vector, ao.bound_box))
bb_center = sum(bbox, Vector((0.0, 0.0, 0.0)))/8.0
ao.location = bb_center * -1
