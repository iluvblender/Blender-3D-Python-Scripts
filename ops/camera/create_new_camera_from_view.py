__author__ = "Satish Goda <satishgoda@live.com>"

import bpy


def main(context):
    C = context

    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(0, -0, 0))

#    area = None
#    for area in C.screen.areas:
#        if area.type == 'VIEW_3D':
#            area = area
#            break

    v3d = context.area.spaces[0]

    camera = C.active_object

    camera.matrix_local = v3d.region_3d.view_matrix.inverted()
    camera.data.lens = v3d.region_3d.view_camera_zoom
    
    C.scene.camera = camera

#    override = {
#        'area': context.area
#    }
    
#    bpy.ops.view3d.view_camera(override)
    bpy.ops.view3d.view_camera()
    


class CreateNewCameraFromViewOperator(bpy.types.Operator):
    """Create new camera from view"""
    bl_idname = "object.camera_create_from_view"
    bl_label = "Create New Camera From View"

    @classmethod
    def poll(cls, context):
        return 'VIEW_3D' in map(lambda area: area.type, context.screen.areas)

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CreateNewCameraFromViewOperator)


def unregister():
    bpy.utils.unregister_class(CreateNewCameraFromViewOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.camera_create_from_view()
