import bpy

ao = bpy.context.active_object

>>> rna_prop = ao.bl_rna.properties['rotation_mode']

>>> rna_prop.identifier
'rotation_mode'

>>> rna_prop.default
'QUATERNION'

>>> rna_prop.default
'QUATERNION'

>>> rna_prop.unit
'NONE'

>>> len(rna_prop.enum_items)
8

>>> rna_prop.enum_items[0]
<bpy_struct, EnumPropertyItem("QUATERNION")>

>>> rna_prop.enum_items[1]
<bpy_struct, EnumPropertyItem("XYZ")>

>>> rna_prop.enum_items[2]
<bpy_struct, EnumPropertyItem("XZY")>

>>> rna_prop.enum_items[3]
<bpy_struct, EnumPropertyItem("YXZ")>

>>> rna_prop.enum_items[4]
<bpy_struct, EnumPropertyItem("YZX")>

>>> rna_prop.enum_items[5]
<bpy_struct, EnumPropertyItem("ZXY")>

>>> rna_prop.enum_items[6]
<bpy_struct, EnumPropertyItem("ZYX")>

>>> rna_prop.enum_items[7]
<bpy_struct, EnumPropertyItem("AXIS_ANGLE")>

>>> rna_prop.enum_items.data
<bpy_struct, EnumProperty("rotation_mode")>

>>> rna_prop
<bpy_struct, EnumProperty("rotation_mode")>

>>> rna_prop_enum_item = rna_prop.enum_items[0]

>>> rna_prop_enum_item.bl_rna
<bpy_struct, Struct("EnumPropertyItem")>

>>> rna_prop_enum_item.rna_type
<bpy_struct, Struct("EnumPropertyItem")>


>>> rna_prop_enum_item.value
0

>>> rna_prop_enum_item.identifier
'QUATERNION'

>>> rna_prop_enum_item.name
'Quaternion (WXYZ)'

>>> rna_prop_enum_item.value
0
