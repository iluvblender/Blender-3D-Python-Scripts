import bpy
from bpy.types import (
    Panel,
)

from bl_ui.properties_workspace import WorkSpaceButtonsPanel



class WORKSPACE_PT_operator(WorkSpaceButtonsPanel, Panel):
    bl_label = "Operators"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("screen.repeat_last")
        layout.operator("screen.repeat_history")


class WORKSPACE_PT_test_operator(WorkSpaceButtonsPanel, Panel):
    bl_label = "Test Operator Development"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.layout_meshes")
        layout.alert = True
        layout.operator_enum("object.layout_meshes", 'axis')
        layout.operator("object.bake_vertex_normal_to_color")


classes = (
    WORKSPACE_PT_operator,
    WORKSPACE_PT_test_operator,
)


if __name__ == "__main__":  # only for live edit.
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
