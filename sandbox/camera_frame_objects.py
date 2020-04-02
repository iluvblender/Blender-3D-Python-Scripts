import bpy

view_layer = bpy.context.view_layer

objects = bpy.context.selected_objects

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
ctx = None
for area in bpy.context.screen.areas:
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
    area = area
    screen = bpy.context.screen

bpy.ops.view3d.camera_to_view_selected()

bpy.ops.object.select_all(action='DESELECT')

## Not working as expected

view_layer.objects.active = camera
view_layer.objects.active.select_set(True, view_layer=view_layer)

orient_matrix = camera.matrix_world.inverted().to_3x3()

bpy.ops.transform.translate(value=(0, 0, -2), 
                            orient_type='LOCAL', 
                            orient_matrix=orient_matrix, 
                            orient_matrix_type='LOCAL', 
                            constraint_axis=(False, False, True), 
                            )


## Not working as expected
if False and found:
    ctx = bpy.context.copy()
    ctx['space_data'] = v3d
    ctx['screen'] = screen
    ctx['area'] = area
    
    bpy.ops.view3d.view_camera(override=ctx)

