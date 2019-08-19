import bpy

for bl_rna_prop in bpy.types.EnumProperty.bl_rna.properties:
    print("{1} ({0}) - {2}".format(bl_rna_prop.name, bl_rna_prop.identifier, bl_rna_prop.description))

"""
rna_type (RNA) - RNA type definition
name (Name) - Human readable name
identifier (Identifier) - Unique name used in the code and scripting
description (Description) - Description of the property for tooltips
translation_context (Translation Context) - Translation context of the property's name
type (Type) - Data type of the property
subtype (Subtype) - Semantic interpretation of the property
srna (Base) - Struct definition used for properties assigned to this item
unit (Unit) - Type of units for this property
icon (Icon) - Icon of the item
is_readonly (Read Only) - Property is editable through RNA
is_animatable (Animatable) - Property is animatable through RNA
is_overridable (Overridable) - Property is overridable through RNA
is_required (Required) - False when this property is an optional argument in an RNA function
is_argument_optional (Optional Argument) - True when the property is optional in a Python function implementing an RNA function
is_never_none (Never None) - True when this value can't be set to None
is_hidden (Hidden) - True when the property is hidden
is_skip_save (Skip Save) - True when the property is not saved in presets
is_output (Return) - True when this property is an output value from an RNA function
is_registered (Registered) - Property is registered as part of type registration
is_registered_optional (Registered Optionally) - Property is optionally registered as part of type registration
is_runtime (Runtime) - Property has been dynamically created at runtime
is_enum_flag (Enum Flag) - True when multiple enums 
is_library_editable (Library Editable) - Property is editable from linked instances (changes not saved)
tags (Tags) - Subset of tags (defined in parent struct) that are set for this property
default (Default) - Default value for this enum
default_flag (Default) - Default value for this enum
enum_items (Items) - Possible values for the property
enum_items_static (Static Items) - Possible values for the property (never calls optional dynamic generation of those)
"""
