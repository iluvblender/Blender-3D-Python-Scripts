import bpy

bpy.context.scene.tool_settings.use_transform_data_origin = True

bpy.ops.transform.translate(value=(-0, -0, -1), 
                            orient_type='GLOBAL', 
                            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                            orient_matrix_type='GLOBAL', 
                            constraint_axis=(False, False, True), 
                            mirror=True, 
                            use_proportional_edit=False, 
                            proportional_edit_falloff='SMOOTH', 
                            proportional_size=1, 
                            use_proportional_connected=False, 
                            use_proportional_projected=False, 
                            release_confirm=True)

bpy.context.scene.tool_settings.use_transform_data_origin = False

bpy.ops.object.location_clear(clear_delta=False)
