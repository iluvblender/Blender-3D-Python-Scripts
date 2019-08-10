import bpy
import bmesh

bpy.ops.object.add(type='MESH')

ao = bpy.context.active_object
ao.name = "Cube"
ao.data.name = "{0}_Lo".format(ao.name)
ao.data.use_fake_user = True

bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(ao.data)
bmesh.ops.create_cube(bm, size=2)
bmesh.update_edit_mesh(ao.data)

bpy.ops.object.mode_set(mode='OBJECT')

meshes = []

# Medium Mesh

mesh = bpy.data.meshes.new("{0}_Med".format(ao.name))
meshes.append(mesh)

ao.data = mesh

bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(ao.data)
bmesh.ops.create_cube(bm, size=2)
bmesh.update_edit_mesh(ao.data)

bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.modifier_add(type='SUBSURF')
subsurf = bpy.context.active_object.modifiers['Subdivision']
subsurf.levels = 1
subsurf.render_levels = 1
bpy.ops.object.modifier_apply(apply_as='DATA', modifier=subsurf.name)

## Hi Mesh

mesh = bpy.data.meshes.new("{0}_Hi".format(ao.name))
meshes.append(mesh)

ao.data = mesh

bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(ao.data)
bmesh.ops.create_cube(bm, size=2)
bmesh.update_edit_mesh(ao.data)

bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.modifier_add(type='SUBSURF')
subsurf = bpy.context.active_object.modifiers['Subdivision']
subsurf.levels = 2
subsurf.render_levels = 2
bpy.ops.object.modifier_apply(apply_as='DATA', modifier=subsurf.name)

for mesh in meshes:
    mesh.use_fake_user = True
