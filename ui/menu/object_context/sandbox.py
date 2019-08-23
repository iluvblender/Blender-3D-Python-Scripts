import bpy


def custom_object_context_menu(self, context):
    layout = self.layout
    layout.label(text="Yessssss")


if not hasattr(bpy.types.VIEW3D_MT_object_context_menu, 'draw_funcs'):
    bpy.types.VIEW3D_MT_object_context_menu.draw_funcs = []
    bpy.types.VIEW3D_MT_object_context_menu.draw_funcs.append(bpy.types.VIEW3D_MT_object_context_menu.draw)
    bpy.types.VIEW3D_MT_object_context_menu.draw = custom_object_context_menu
    
else:
    bpy.types.VIEW3D_MT_object_context_menu.draw = bpy.types.VIEW3D_MT_object_context_menu.draw_funcs[0]
