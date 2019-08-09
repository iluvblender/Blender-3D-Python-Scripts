import bpy
from mathutils import Vector

##### Create a simple scene

# Create new material
myMaterial = bpy.data.materials.new('MyMaterial')

# Create mesh using that material
myMesh = bpy.data.meshes.new('MyMesh')
myMesh.materials.append(myMaterial)

# Add vertices and faces to mesh
myMesh.from_pydata(
    [ Vector([1,0,0]), Vector([0,1,0]), Vector([0,0,1]), Vector([0,0,0])], # Vertices
    [], # No Edges
    [ (0,1,2) ]) # Faces

# Create object using that mesh
myObject = bpy.data.objects.new('MyObject', myMesh)

myCollection = bpy.data.collections.new(collectionName)
myCollection.objects.link(myObject)
bpy.context.scene.collection.children.link(myCollection)

# Make the object the active object and select it
bpy.context.view_layer.objects.active = myObject
myObject.select_set(True)

# We are adding a subdivision surface operator.
# This operator works in the object mode and on the active object
bpy.ops.object.modifier_add(type='SUBSURF')

# Now we change the properties of the subdivision surface
bpy.context.object.modifiers["Subdivision"].levels = 2

# Then we apply the modifier
bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
