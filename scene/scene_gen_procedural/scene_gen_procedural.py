import bpy
from mathutils import Vector

##### Clean-up results from an earlier run of the script

# Delete previously created collection if present

collectionName = 'MyCollection'
if collectionName in bpy.data.collections:
    bpy.data.collections.remove(bpy.data.collections[collectionName])

# Helper code. Is this part of the standard API?
def garbage_collect():
    found_garbage = True
    while found_garbage:
        found_garbage = False
        for things in [ bpy.data.collections,
                        bpy.data.meshes,
                        bpy.data.objects,
                        bpy.data.materials,
                        bpy.data.textures,
                        bpy.data.images ]:
            for block in things:
                if block.users == 0:
                    things.remove(block)
                    found_garbage = True

# Garbage collect so that objects which became orphaned when
# deleting the collection actually disappear.
#
# Note that the names of meshes, objects, ... must be unique in blender.
# Calling, e.g., bpy.data.materials.new('MyMaterial') will name
# the new material MyMaterial.001, MyMaterial.002 if MyMaterial
# already existed.
# Running this script several times would create materials with
# those names if we did not call garbage collect here.

garbage_collect()

##### Create a simple scene

# Create new material
myMaterial = bpy.data.materials.new('MyMaterial')

# Create mesh using that material
myMesh = bpy.data.meshes.new('MyMesh')
myMesh.materials.append(myMaterial)

# Add vertices and faces to mesh
#
# A potential bug:
# Note that you would expect that the three edges
# specified below should be the three line segments
# connecting the origin to each of the three vertices
# of the triangle - but there seems to be a bug and
# only two of those edges appear.
myMesh.from_pydata(
    [ Vector([1,0,0]), # Vertices
      Vector([0,1,0]),
      Vector([0,0,1]),
      Vector([0,0,0])],
    [ (0,3),           # Edges
      (1,3),
      (2,3) ],
    [ (0,1,2) ])       # Faces

# Create object using that mesh
myObject = bpy.data.objects.new('MyObject', myMesh)

# A subtle note:
# Note that we can change the mesh later with
# myOtherMesh = bpy.data.meshes.new('MyOtherMesh')
# myObject.data = myOtherMesh
#
# However, we cannot create an empty object and then
# attach a mesh to it later, so the following code will fail:
# myObject = bpy.data.objects.new('MyObject', None)
# myObject.data = myMesh
# Is there a way to change the type of an object later or
# specify the type as mesh when calling bpy.data.objects.new without
# giving a mesh?

# Create collection using that object
myCollection = bpy.data.collections.new(collectionName)
myCollection.objects.link(myObject)

# Add collection to scene collection
bpy.context.scene.collection.children.link(myCollection)

