__author__ = 'Satish Goda <satishgoda@live.com>'


import bpy


############### Generating Stacked Cubes ###############

# Remove any unused data (reference count is zero)
bpy.ops.outliner.orphans_purge()


# The object that we are going to use to build 
# the active rigid bodies from

size = 0.2
bpy.ops.mesh.primitive_cube_add(size=size, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(0, 0, 0))


# Since we created the cube, it becomes the active_object
active_object = bpy.context.active_object


# Position it on the positive x, y, z quadrant
bpy.context.object.location = (size/2, size/2, size/2)

# We are going to use three array modifiers to procedurally 
# generate the duplicated meshes first.

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

# Apply the modifiers so that we get one mesh with 
# separate cube meshes organized in a 3D grid

for modifier in active_object.modifiers:    
    bpy.ops.object.modifier_apply(apply_as='DATA', 
                                  modifier=modifier.name)

# Separate the cube meshes in the main mesh 

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

# Make sure the pivots of the generated objects is at the right place

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')


# Let us make sure all the meshes share the same mesh data,
# to save memory and also improve performance.

bpy.ops.object.make_links_data(type='OBDATA')


############### Rigid Body Dynamics ###############
# So we now have a stacked bunch of cubes selected.
# Time for make them rigid bodies


# Create the collection for storing active rigid bodies

def get_or_create_collection(name):
    if bpy.data.collections.find(name) == -1:
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections[name]
    return collection


active_rbd_collection = get_or_create_collection('Active Rigid Bodies')
passive_rbd_collection = get_or_create_collection('Passive Rigid Bodies')


# Make the generated meshes as active rigid bodies

bpy.ops.rigidbody.objects_add(type='ACTIVE')


# Link the active rigid bodies to the appropriate collection
# Also remove them from the "Scene Collection" to keep the outliner clean

active_rbd_objects = bpy.context.selected_objects
for obj in active_rbd_objects:
    # Modify some rigid body specific settings
    rbd_settings = obj.rigid_body
    
    rbd_settings.restitution = 0.865672

    active_rbd_collection.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)


# Create a groundplane

bpy.ops.mesh.primitive_plane_add(size=10, 
                                 enter_editmode=False, 
                                 align='WORLD', 
                                 location=(0, 0, 0))

groundplane = bpy.context.active_object


# And make it into a passive rigid body

bpy.ops.rigidbody.object_add(type='PASSIVE')


# Modify some rigid body specific settings

rbd_settings = groundplane.rigid_body

rbd_settings.use_margin = True
rbd_settings.collision_margin = 0.001
rbd_settings.restitution = .5


# Link the passive rigid bodies

passive_rbd_collection.objects.link(groundplane)
bpy.context.scene.collection.objects.unlink(groundplane)


############### Switch Workspaces ###############

# At the moment we are in the "Scripting" workspace. We are going to 
# switch over to the "Layout" workspace to perform rest of the operations

workspace_layout = bpy.data.workspaces['Layout']

bpy.context.window.workspace = workspace_layout


# We are going to use the view_layer to select objects and 
# set active object

view_layer = bpy.context.view_layer


# We are going to be setting scene properties

scene = bpy.context.scene


# Let's add a camera to the scene. It will be placed in the 

bpy.ops.object.camera_add()

camera = bpy.context.active_object


# Make the camera current scene's active camera

scene.camera = camera


# Deselect everything in the scene

bpy.ops.object.select_all(action='DESELECT')


# Select all the active rigid body objects (stacked cubes)

for object in active_rbd_objects:
    view_layer.objects.active = object
    view_layer.objects.active.select_set(True, view_layer=view_layer)


# And then select the camera object (it becomes the active object)

view_layer.objects.active = camera
view_layer.objects.active.select_set(True, view_layer=view_layer)


# Set the end frame for the scene and the rigid body world 

frame_end = 300
scene.frame_end = frame_end
scene.rigidbody_world.point_cache.frame_end = frame_end


def get_screen_area_3d(screen):
    """
    Locate the first available 3d view in the given screen
    """
    area_3D = None
    for area in screen.areas:
        if not area.type == 'VIEW_3D':
            continue
        # If we reach here, we found a 3D view!
        # So let us exit out of the loop
        area_3D = area
        break
    return area_3D

area = get_screen_area_3d(workspace_layout.screens[0])


# We now move the scene camera to match the current user perspective

v3d = area.spaces[0]


# Move the scenes'camera to where the user perspective camera is

camera.matrix_local = v3d.region_3d.view_matrix.inverted()
camera.data.lens = v3d.region_3d.view_camera_zoom


# We are preparing a custom execution context so that the next
# operator can run in the 3D view 

ctx = {}

ctx.update((
            ('area', area),
          ))


# Frame the active camera object to fit all the stacked cubes

bpy.ops.view3d.camera_to_view_selected()


# Deselect everything

bpy.ops.object.select_all(action='DESELECT')

# Select only the camera

view_layer.objects.active = camera
view_layer.objects.active.select_set(True, view_layer=view_layer)


# Get the matrix so that we can move the camera in local space

orient_matrix = camera.matrix_world.inverted().to_3x3()


# Move the camera x units away (on its local z axis) from the stacked cubes

move_camera_away = True
move_away_by = 3

if move_camera_away:
    bpy.ops.transform.translate(value=(0, 0, move_away_by), 
                                orient_type='LOCAL',
                                orient_matrix=orient_matrix,
                                constraint_axis=(False, False, True), 
                                )

# Let the viewport use the scene camera

bpy.ops.view3d.view_camera(ctx)


# Update the 3D View to render using the camera

area = get_screen_area_3d(workspace_layout.screens[0])
area.spaces[0].region_3d.view_perspective = 'CAMERA'


# Remove any unused data (reference count is zero)

bpy.ops.outliner.orphans_purge()


# Play Animation

bpy.ops.screen.frame_jump(end=False)
bpy.ops.screen.animation_play()
