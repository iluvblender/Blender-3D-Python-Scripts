import bpy


def custom_object_context_menu(self, context):
    layout = self.layout
    layout.label(text="Yessssss")


if not hasattr(bpy.types.VIEW3D_MT_object_context_menu, 'draw_funcs'):
    draw_funcs = bpy.types.VIEW3D_MT_object_context_menu.draw_funcs = []
    draw_default = bpy.types.VIEW3D_MT_object_context_menu.draw
    draw_funcs.append(draw_default)
    bpy.types.VIEW3D_MT_object_context_menu.draw = custom_object_context_menu
else:
    draw_default = bpy.types.VIEW3D_MT_object_context_menu.draw_funcs[0]
    bpy.types.VIEW3D_MT_object_context_menu.draw = draw_default
    delattr(bpy.types.VIEW3D_MT_object_context_menu, 'draw_funcs')
