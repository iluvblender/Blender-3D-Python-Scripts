import bpy


class LayoutMeshesOperator(bpy.types.Operator):
    """Lays out selected Mesh objects on the X-axis"""
    bl_idname = "object.layout_meshes"
    bl_label = "Layout Mesh objects on X-axis"

    @classmethod
    def poll(cls, context):
        return context.selected_objects and \
               len(context.selected_objects) > 1 and \
               all(map(lambda obj: obj.type =='MESH', 
                   context.selected_objects)
                   )

    def execute(self, context):
        ao = context.active_object

        other_objects = set(context.selected_objects) - set([ao])

        gap = 0.0
        offset = ao.dimensions.x/2.0 + gap

        for obj in other_objects:
            adjust = obj.dimensions.x/2.0 
            obj.location.x = offset + adjust
            offset = obj.location.x + adjust + gap

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LayoutMeshesOperator)


def unregister():
    bpy.utils.unregister_class(LayoutMeshesOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.layout_meshes()
