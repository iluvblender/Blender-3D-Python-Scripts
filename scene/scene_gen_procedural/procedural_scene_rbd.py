import bpy

# Remove any unused data (reference count is zero)
bpy.ops.outliner.orphans_purge()

## The object that we are going to use to build 
## the active rigid bodies from

size = 0.2
bpy.ops.mesh.primitive_cube_add(size=size, 
                                enter_editmode=False, 
                                align='WORLD', 
                                location=(0, 0, 0))

# Position it on the positive x, y, z quadrant

bpy.context.object.location = (size/2, size/2, size/2)

## We are going to use three array modifiers to procedurally 
## generate the duplicated meshes first.

axes_offset_displace = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    )

for axes in range(0, 3):
    bpy.ops.object.modifier_add(type='ARRAY')
    bpy.context.active_object.modifiers[-1].use_relative_offset = True
    bpy.context.active_object.modifiers[-1].relative_offset_displace = axes_offset_displace[axes]
    bpy.context.active_object.modifiers[-1].count = 5

# Apply the modifiers so that we get one mesh with 
# separate cube meshes organized in a 3D grid

for modifier in bpy.context.active_object.modifiers:    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)

## Separate the cube meshes in the main mesh 

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.separate(type='LOOSE')
bpy.ops.object.mode_set(mode='OBJECT')

## Make sure the pivots of the generated objects is at the right place

bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

## Let us make sure all the meshes share the same mesh data,
## to save memory and also improve performance.

bpy.ops.object.make_links_data(type='OBDATA')

objects = bpy.context.selected_objects

## Rigid Body Dynamics

# Create the collection for storing active rigid bodies

if bpy.data.collections.find('Active Rigid Bodies') == -1:
    active_rbd_collection = bpy.data.collections.new('Active Rigid Bodies')
    bpy.context.scene.collection.children.link(bpy.data.collections['Active Rigid Bodies'])
else:
    active_rbd_collection = bpy.data.collections['Active Rigid Bodies']

# Create the collection for storing passive rigid bodies

if bpy.data.collections.find('Passive Rigid Bodies') == -1:
    passive_rbd_collection = bpy.data.collections.new('Passive Rigid Bodies')
    bpy.context.scene.collection.children.link(bpy.data.collections['Passive Rigid Bodies'])
else:
    passive_rbd_collection = bpy.data.collections['Passive Rigid Bodies']


# Make the generated meshes as active rigid bodies

bpy.ops.rigidbody.objects_add(type='ACTIVE')

# Link the active rigid bodies
# Also remove them from the Scene Collection to keep the outliner clean

for obj in objects:
    active_rbd_collection.objects.link(obj)
    bpy.context.scene.collection.objects.unlink(obj)

# Create a plane that will be our passive rigid body

bpy.ops.mesh.primitive_plane_add(size=10, 
                                 enter_editmode=False, 
                                 align='WORLD', 
                                 location=(0, 0, 0))

bpy.ops.rigidbody.object_add(type='PASSIVE')
bpy.context.active_object.rigid_body.use_margin = True
bpy.context.active_object.rigid_body.collision_margin = 0.01

# Link the passive rigid bodies

passive_rbd_collection.objects.link(bpy.context.active_object)
bpy.context.scene.collection.objects.unlink(bpy.context.active_object)


## Switch Workspaces

bpy.context.window.workspace = bpy.data.workspaces['Layout']
bpy.context.window.workspace.tag = True

view_layer = bpy.context.view_layer

bpy.ops.object.camera_add()

camera = bpy.context.active_object

bpy.ops.object.select_all(action='DESELECT')


for object in objects:
    view_layer.objects.active = object
    view_layer.objects.active.select_set(True, view_layer=view_layer)

view_layer.objects.active = camera

view_layer.objects.active.select_set(True, view_layer=view_layer)

bpy.context.scene.camera = camera

found = False
ctx = {}
for area in bpy.context.window.workspace.screens[0].areas:
    if found:
        break
    if not area.type == 'VIEW_3D':
        continue
    found = True
    
    v3d = area.spaces[0]
    camera.matrix_local = v3d.region_3d.view_matrix.inverted()
    camera.data.lens = v3d.region_3d.view_camera_zoom
    #v3d.camera = camera
    #v3d.use_local_camera = True
    #v3d.region_3d.view_perspective = 'PERSP'
    area_ = area
    window = bpy.context.window
    #screen = bpy.context.screen
    region = area.regions[5]
    workspace = bpy.data.workspaces['Layout']
    
    ctx.update((
        ('window', window),
        ('workspace', workspace),
        #('screen', screen),
        ('area', area_),
        ('space_data',v3d),
        ('region', region),
        ('active_object', camera),
    ))

bpy.ops.view3d.camera_to_view_selected()

bpy.ops.object.select_all(action='DESELECT')

view_layer.objects.active = camera
view_layer.objects.active.select_set(True, view_layer=view_layer)

orient_matrix = camera.matrix_world.inverted().to_3x3()

bpy.ops.transform.translate(value=(0, 0, 3), 
                            orient_type='LOCAL',
                            orient_matrix=orient_matrix,
                            constraint_axis=(False, False, True), 
                            )


bpy.ops.view3d.view_camera(ctx, 'EXEC_REGION_WIN')

bpy.data.workspaces['Layout'].screens['Layout'].areas[3].spaces[0].region_3d.view_perspective = 'CAMERA'

## Play Animation

bpy.ops.screen.frame_jump(end=False)
bpy.ops.screen.animation_play()
