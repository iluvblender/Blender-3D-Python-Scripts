import bpy

camera_scene = bpy.context.scene.camera

t, rQ, s = camera_scene.matrix_world.decompose()

ao = bpy.context.active_object

ao.rotation_mode = 'QUATERNION'

ao.rotation_quaternion = rQ
