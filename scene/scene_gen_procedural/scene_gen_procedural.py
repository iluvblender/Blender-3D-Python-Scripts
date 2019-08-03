__author__ = 'Satish Goda <satishgoda@live.com>'

import bpy


def deselect_all():
    vl = bpy.context.view_layer
    for obj in bpy.context.view_layer.objects:
        obj.select_set(False, view_layer=vl)

## Create a new collection
coll = bpy.data.collections.new("shapes2")

## Link the new collection to the scene collection
bpy.context.scene.collection.children.link(coll)

## Get the index of the new collection
coll_index = bpy.context.scene.collection.children.find(coll.name)

## Create a null object (known as EMPTY in Blender)
bpy.ops.object.add()

## Move the null object to the new collection
bpy.ops.object.move_to_collection(collection_index=coll_index+1)

## Save a handle to the null object
null_obj = bpy.context.active_object

## Increase the size of the null object display size
null_obj.empty_display_size = 3

## Create a Cube mesh object
bpy.ops.mesh.primitive_cube_add()

## Link to collection
bpy.ops.object.move_to_collection(collection_index=coll_index+1)

## Handle
mesh_obj = bpy.context.active_object

## Parenting
mesh_obj.parent = null_obj

## Make sure everything else is deselected
null_obj.select_set(False)

## Select the mesh to which we are going to add a material
mesh_obj.select_set(True)

## Create a material slot for the mes
bpy.ops.object.material_slot_add()

## Create the material
greenMtl = bpy.data.materials.new('green')

## Set the diffuse color
greenMtl.diffuse_color[0] = 0
greenMtl.diffuse_color[1] = 1
greenMtl.diffuse_color[2] = 0

## Get the first material slot
slot = mesh_obj.material_slots[0]

## You can link the material to the object or its data
slot.link = 'OBJECT'
#slot.link = 'DATA'

## Link the material to the slot
slot.material = greenMtl

## Select the null object only
deselect_all()
bpy.context.view_layer.objects.active = null_obj
null_obj.select_set(True)


