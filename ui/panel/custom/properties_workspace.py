class WORKSPACE_PT_operator(WorkSpaceButtonsPanel, Panel):
    bl_label = "Operators"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("screen.repeat_last")
        layout.operator("screen.repeat_history")
        
classes = (
    ....,
    WORKSPACE_PT_operator,
    ....,
)
