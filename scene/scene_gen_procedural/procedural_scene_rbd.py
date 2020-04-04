__author__ = 'Satish Goda <satishgoda@live.com>'

"""
Generates a Blender scene programmatically using Python.
https://www.youtube.com/watch?v=-noHVVWXMWM
"""

import bpy

bpy.ops.outliner.orphans_purge()

size = 0.2
bpy.ops.mesh.primitive_cube_add(size=size, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(0, 0, 0))

active_object = bpy.context.active_object

bpy.context.object.location = (size/2, size/2, size/2)

axes_offset_displace = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    )

for axes in range(0, 3):
    bpy.ops.object.modifier_add(type='ARRAY')
    modifier = active_object.modifiers[-1]
    modifier.use_relative_offset = True
    modifier.relative_offset_displace = axes_offset_displace[axes]
    modifier.count = 5

for modifier in active_object.modifiers:    
    bpy.ops.object.modifier_apply(apply_as='DATA', 
                                  modifier=modifier.name)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

bpy.ops.object.make_links_data(type='OBDATA')

def get_or_create_collection(name):
    if bpy.data.collections.find(name) == -1:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections[name]
    return collection


active_rbd_collection = get_or_create_collection('Active Rigid Bodies')
passive_rbd_collection = get_or_create_collection('Passive Rigid Bodies')

bpy.ops.rigidbody.objects_add(type='ACTIVE')

active_rbd_objects = bpy.context.selected_objects
for obj in active_rbd_objects:
    rbd_settings = obj.rigid_body
    rbd_settings.restitution = 0.865672
    active_rbd_collection.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)

bpy.ops.mesh.primitive_plane_add(size=10, 
                                 enter_editmode=False, 
                                 align='WORLD', 
                                 location=(0, 0, 0))

groundplane = bpy.context.active_object

bpy.ops.rigidbody.object_add(type='PASSIVE')

rbd_settings = groundplane.rigid_body
rbd_settings.use_margin = True
rbd_settings.collision_margin = 0.001
rbd_settings.restitution = .5

passive_rbd_collection.objects.link(groundplane)
bpy.context.scene.collection.objects.unlink(groundplane)

workspace_layout = bpy.data.workspaces['Layout']

bpy.context.window.workspace = workspace_layout

view_layer = bpy.context.view_layer

scene = bpy.context.scene

bpy.ops.object.camera_add()

camera = bpy.context.active_object

scene.camera = camera

bpy.ops.object.select_all(action='DESELECT')

for object in active_rbd_objects:
    view_layer.objects.active = object
    view_layer.objects.active.select_set(True, view_layer=view_layer)

view_layer.objects.active = camera
view_layer.objects.active.select_set(True, view_layer=view_layer)

frame_end = 300
scene.frame_end = frame_end
scene.rigidbody_world.point_cache.frame_end = frame_end

def get_screen_area_3d(screen):
    area_3D = None
    for area in screen.areas:
        if not area.type == 'VIEW_3D':
            continue
        area_3D = area
        break
    return area_3D

area = get_screen_area_3d(workspace_layout.screens[0])

v3d = area.spaces[0]
camera.matrix_local = v3d.region_3d.view_matrix.inverted()
camera.data.lens = v3d.region_3d.view_camera_zoom

ctx = {}
ctx.update((
            ('area', area),
          ))

bpy.ops.view3d.camera_to_view_selected()

bpy.ops.object.select_all(action='DESELECT')

view_layer.objects.active = camera
view_layer.objects.active.select_set(True, view_layer=view_layer)

orient_matrix = camera.matrix_world.inverted().to_3x3()

move_camera_away = True
move_away_by = 3

if move_camera_away:
    bpy.ops.transform.translate(value=(0, 0, move_away_by), 
                                orient_type='LOCAL',
                                orient_matrix=orient_matrix,
                                constraint_axis=(False, False, True), 
                                )

bpy.ops.view3d.view_camera(ctx)

area = get_screen_area_3d(workspace_layout.screens[0])
area.spaces[0].region_3d.view_perspective = 'CAMERA'

bpy.ops.outliner.orphans_purge()

bpy.ops.screen.frame_jump(end=False)
bpy.ops.screen.animation_play()
