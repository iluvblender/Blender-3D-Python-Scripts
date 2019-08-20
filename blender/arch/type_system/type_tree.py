import bpy

text = bpy.data.texts['output.txt']

for cls in bpy.types.bpy_struct.__subclasses__():
    text.write("{0} - {1}".format(cls, cls.__bases__))
    text.write("\n")
