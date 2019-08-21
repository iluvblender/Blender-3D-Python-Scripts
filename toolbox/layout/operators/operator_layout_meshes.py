import bpy
from bpy.props import FloatProperty


class LayoutMeshesOperator(bpy.types.Operator):
    """Lays out selected Mesh objects on the X-axis"""
    bl_idname = "object.layout_meshes"
    bl_label = "Layout Mesh objects on X-axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    gap: FloatProperty(
        name='Gap',
        description="Extra gap between meshes",
        min=0.0, max=10,
        default=0.0
    )

    @classmethod
    def poll(cls, context):
        return context.selected_objects and \
               len(context.selected_objects) > 1 and \
               all(map(lambda obj: obj.type =='MESH', 
                   context.selected_objects)
                   )

    def execute(self, context):
        ao = context.active_object
        selected_objects = context.selected_objects
        index = selected_objects.index(ao)
        selected_objects.pop(index)

        offset = ao.bound_box[4][0] + self.gap

        for obj in selected_objects:
            obj.location.x = offset + abs(obj.bound_box[0][0])
            offset = obj.location.x + abs(obj.bound_box[4][0]) + self.gap

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LayoutMeshesOperator)


def unregister():
    bpy.utils.unregister_class(LayoutMeshesOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.layout_meshes()
