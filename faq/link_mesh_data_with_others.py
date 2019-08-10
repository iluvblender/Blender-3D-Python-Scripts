import bpy

active_object = bpy.context.active_object

# Ignore the last element of the list (which is the active object)
selected_objects = bpy.context.selected_objects[:-1]

if not selected_objects:
    raise ValueError("Only one object selected")

meshes_to_remove = set()

for item in selected_objects:
    meshes_to_remove.add(item.data)
    item.data = active_object.data

for mesh in meshes_to_remove:
    # If the mesh is still being used by other objects,
    # or if the user explicitly wants to keep the mesh around,
    # let us not remove it
    if mesh.users or mesh.use_fake_user:
        continue

    # If we are here, we are safe to remove the mesh
    print("removing ", mesh)
    bpy.data.meshes.remove(mesh)

