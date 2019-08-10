import bpy
import bmesh

# Add Empty Mesh
bpy.ops.object.add(type='MESH')

ao = bpy.context.active_object
ao.name = "Cube"

bpy.ops.object.mode_set(mode='EDIT')

mesh = ao.data
mesh.name = "{0}_Lo".format(ao.name)
#mesh.use_fake_user = True

bm = bmesh.from_edit_mesh(mesh)
bmesh.ops.create_cube(bm, size=2)

bmesh.update_edit_mesh(mesh)

bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.modifier_add(type='SUBSURF')
subsurf = bpy.context.active_object.modifiers['Subdivision']
subsurf.levels = 0
subsurf.render_levels = 0

bpy.ops.object.modifier_apply(apply_as='DATA')

mesh = None

mesh = bpy.data.meshes.new("{0}_Med".format(ao.name))
#mesh.use_fake_user = True
bpy.context.view_layer.objects.active = ao
ao.select_set(True)
ao.data = mesh

bpy.ops.object.mode_set(mode='EDIT')

mesh = ao.data

bm = bmesh.from_edit_mesh(mesh)
bmesh.ops.create_cube(bm, size=2)

bmesh.update_edit_mesh(mesh)

bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.modifier_add(type='SUBSURF')
subsurf = bpy.context.active_object.modifiers['Subdivision']
subsurf.levels = 1
subsurf.render_levels = 1

bpy.ops.object.modifier_apply(apply_as='DATA')

mesh = None

mesh = bpy.data.meshes.new("{0}_Hi".format(ao.name))
#mesh.use_fake_user = True
bpy.context.view_layer.objects.active = ao
ao.select_set(True)
ao.data = mesh

bpy.ops.object.mode_set(mode='EDIT')

mesh = ao.data

bm = bmesh.from_edit_mesh(mesh)
bmesh.ops.create_cube(bm, size=2)

bmesh.update_edit_mesh(mesh)

bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.modifier_add(type='SUBSURF')
subsurf = bpy.context.active_object.modifiers['Subdivision']
subsurf.levels = 2
subsurf.render_levels = 2

bpy.ops.object.modifier_apply(apply_as='DATA')
