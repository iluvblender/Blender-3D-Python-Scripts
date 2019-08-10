import bpy
import bmesh

# Add Empty Mesh
bpy.ops.object.add(type='MESH')

# Switch to edit mode for the object
bpy.ops.object.mode_set(mode='EDIT')

# Get the mesh data for the object
mesh = bpy.context.active_object.data

# Convert to bmesh and then generate a cube mesh
bm = bmesh.from_edit_mesh(mesh)
bmesh.ops.create_cube(bm, size=2)

# Update edit mesh with the generated mesh
bmesh.update_edit_mesh(mesh)

# Switch back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Add a modifier and set view levels to 2
bpy.ops.object.modifier_add(type='SUBSURF')
bpy.context.active_object.modifiers['Subdivision'].levels = 2

# Set smooth shading
bpy.ops.object.shade_smooth()
