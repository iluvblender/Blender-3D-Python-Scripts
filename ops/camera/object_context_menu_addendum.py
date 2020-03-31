__author__ = 'Satish Goda <satishgoda@live.com>'

# Adds custom menu items to the Object mode context menu


import bpy


def menu_func(self, context):
    if not context.active_object.type == 'CAMERA':
        return

    self.layout.separator()

    self.layout.operator(
        'view3d.object_as_camera',
        icon='PLUGIN')


def register():
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()
