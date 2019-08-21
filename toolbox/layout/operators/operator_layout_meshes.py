import bpy
from bpy.props import FloatProperty, EnumProperty


class LayoutMeshesOperator(bpy.types.Operator):
    """Lays out selected Mesh objects on the a selected axis"""
    bl_idname = "object.layout_meshes"
    bl_label = "Layout Mesh objects on X/Y/Z axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    axis: EnumProperty(
        name="Axis of Alignment",
        description="Axis along which alignment operation will take place",
        default="X",
        items=(
        ('X', 'X-Axis', 'X Axis'),
        ('Y', 'Y-Axis', 'Y Axis'),
        ('Z', 'Z-Axis', 'Z Axis')
        )
    )
    
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
        
        axes_index = {
            'X': 0,
            'Y': 1,
            'Z': 2
        }
        
        bbox_axes_index = {
            'min': {
                'X': 0,
                'Y': 4,
                'Z': 7
            },
            'max': {
                'X': 4,
                'Y': 7,
                'Z': 6
            }
        }
        
        offset = ao.location[axes_index[self.axis]] + ao.bound_box[bbox_axes_index['max'][self.axis]][axes_index[self.axis]] + self.gap

        for obj in selected_objects:
            other_axes = axes_index.copy()
            other_axes.pop(self.axis)

            for axis in other_axes.values():
                obj.location[axis] = ao.location[axis]

            obj.location[axes_index[self.axis]] = offset + abs(obj.bound_box[bbox_axes_index['min'][self.axis]][axes_index[self.axis]])
            offset = obj.location[axes_index[self.axis]] + abs(obj.bound_box[bbox_axes_index['max'][self.axis]][axes_index[self.axis]]) + self.gap

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LayoutMeshesOperator)


def unregister():
    bpy.utils.unregister_class(LayoutMeshesOperator)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.layout_meshes()
