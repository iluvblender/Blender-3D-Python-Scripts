import bpy

size = 0.2

bpy.ops.mesh.primitive_cube_add(size=size, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(0, 0, 0))

bpy.context.object.location = (size/2, size/2, size/2)

axes_offset_displace = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    )

## Modifiers

for axes in range(0, 3):
    bpy.ops.object.modifier_add(type='ARRAY')
    bpy.context.active_object.modifiers[-1].use_relative_offset = True
    bpy.context.active_object.modifiers[-1].relative_offset_displace = axes_offset_displace[axes]
    bpy.context.active_object.modifiers[-1].count = 5

for modifier in bpy.context.active_object.modifiers:    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)

## Generate Objects 

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
bpy.ops.object.make_links_data(type='OBDATA')

## Rigid Body Dynamics

bpy.ops.rigidbody.objects_add(type='ACTIVE')

if bpy.data.collections.find('Active Rigid Bodies') == -1:
    active_rbd_collection = bpy.data.collections.new('Active Rigid Bodies')
    bpy.context.scene.collection.children.link(bpy.data.collections['Active Rigid Bodies'])
else:
    active_rbd_collection = bpy.data.collections['Active Rigid Bodies']

for obj in bpy.context.selected_objects:
    active_rbd_collection.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)

bpy.ops.mesh.primitive_plane_add(size=10, 
                                 enter_editmode=False, 
                                 align='WORLD', 
                                 location=(0, 0, 0))

if bpy.data.collections.find('Passive Rigid Bodies') == -1:
    passive_rbd_collection = bpy.data.collections.new('Passive Rigid Bodies')
    bpy.context.scene.collection.children.link(bpy.data.collections['Passive Rigid Bodies'])
else:
    passive_rbd_collection = bpy.data.collections['Passive Rigid Bodies']

passive_rbd_collection.objects.link(bpy.context.active_object)
bpy.context.scene.collection.objects.unlink(bpy.context.active_object)

bpy.ops.rigidbody.object_add(type='PASSIVE')

bpy.context.active_object.rigid_body.use_margin = True
bpy.context.active_object.rigid_body.collision_margin = 0.01

## 3D View Settings

for area in bpy.context.screen.areas:
    if not area.type == 'VIEW_3D':
        continue
    space_data = area.spaces[0]
    space_data.overlay.show_wireframes = True

## Switch Workspaces

bpy.context.window.workspace = bpy.data.workspaces['Layout']

## Play Animation

bpy.ops.screen.frame_jump(end=False)
bpy.ops.screen.animation_play()
