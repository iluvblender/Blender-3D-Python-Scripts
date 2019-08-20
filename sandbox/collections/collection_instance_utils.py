import bpy
from mathutils import Vector


def get_combined_dimensions():
    scene_object = bpy.context.active_object

    if not scene_object.instance_type == 'COLLECTION':
        raise ValueError("Active object must be a collection instance")

    instance_objects = scene_object.instance_collection.objects

    bboxes = map(lambda obj: obj.bound_box,instance_objects)
    dims = map(lambda obj: obj.dimensions, instance_objects)

    dim_combined = Vector(map(max, zip(*dims)))
    
    return dim_combined


def adjust_location_using_dimension(axes, dimension_vector):
    if not axes in ('x', 'y', 'z'):
        raise ValueError("Axes must be in 'x'/'y'/'z'")

    if not isinstance(dimension_vector, Vector):
        raise ValueError("dimension_vector must be mathutils.Vector instance")

    scene_object = bpy.context.active_object

    if axes == 'x':
        scene_object.location.x = dimension_vector.x / 2.0
    elif axes == 'y':
        scene_object.location.y = dimension_vector.y / 2.0
    elif axes == 'z':
        scene_object.location.z = dimension_vector.z / 2.0
