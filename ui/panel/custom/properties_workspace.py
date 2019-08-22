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
        
classes = (
    ....,
    WORKSPACE_PT_operator,
    WORKSPACE_PT_test_operator,
    ....,
)
