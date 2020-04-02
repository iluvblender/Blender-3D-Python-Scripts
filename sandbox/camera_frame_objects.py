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
    v3d.region_3d.view_perspective = 'CAMERA'
    camera.matrix_local = v3d.region_3d.view_matrix.inverted()
    camera.data.lens = v3d.region_3d.view_camera_zoom
    #v3d.camera = camera
    #v3d.use_local_camera = True
    area = area
    area.tag_redraw()
    window = bpy.context.window
    screen = bpy.context.screen
    region = area.regions[5]
    print(region.type)

bpy.ops.view3d.camera_to_view_selected()

bpy.ops.object.select_all(action='DESELECT')

view_layer.objects.active = camera
view_layer.objects.active.select_set(True, view_layer=view_layer)

#if found:
#    ctx = {}
#    ctx.update((
#            ('active_object', camera),
#            ('space_data',v3d),
#            ('screen', screen),
#            ('window', window),
#            ('region', region),
#        ))
#    bpy.ops.view3d.view_camera(ctx)

#orient_matrix = camera.matrix_world.inverted().to_3x3()

#bpy.ops.transform.translate(value=(0, 0, -2), 
#                            orient_type='LOCAL', 
#                            orient_matrix=orient_matrix, 
#                            orient_matrix_type='LOCAL', 
#                            constraint_axis=(False, False, True), 
#                            )
