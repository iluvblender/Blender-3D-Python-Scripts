import bpy


def update_modify_camera(self, context):
    if self.modify_camera:
        context.scene.camera.data.clip_start = self.start
        context.scene.camera.data.clip_end = self.end


def update_start(self, context):
    scene = context.scene

    if self.modify_camera:
        scene.camera.data.clip_start = self.start

    scene.eevee.volumetric_start = self.start


def update_end(self, context):
    scene = context.scene

    if self.modify_camera:
        scene.camera.data.clip_end = self.end

    scene.eevee.volumetric_end = self.end


class VolumetricsClipAdjust(bpy.types.Operator):
    """Adjust the clipping distance of the volumetrics engine"""
    bl_idname = "scene.eevee_volumetric_range"
    bl_label = "Adjust Eevee Volumetrics Range"

    start: bpy.props.FloatProperty(update=update_start, min=0.0)
    end: bpy.props.FloatProperty(update=update_end, min=0.0)
    
    modify_camera = bpy.props.BoolProperty(update=update_modify_camera, default=True)

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'BLENDER_EEVEE' and bool(context.scene.camera)

    def execute(self, context):
        scene = context.scene

        return {'FINISHED'}
    
    def draw(self, context):
        scene = context.scene
        
        layout = self.layout

        row = layout.row()
        row.prop(scene.eevee, 'use_volumetric_lights')

        if scene.eevee.use_volumetric_lights:
            row.prop(scene.eevee, 'use_volumetric_shadows')
            box = layout.box()
            box.prop(self, 'start')
            box.prop(self, 'end')
            box.prop(self, 'modify_camera')
            if not self.modify_camera:
                box.prop(scene.camera.data, 'clip_start')
                box.prop(scene.camera.data, 'clip_end')
            row = layout.row()
            row.props_enum(scene.eevee, 'volumetric_tile_size')
            row = layout.row()
            row.prop(scene.eevee, 'volumetric_samples')
            row.prop(scene.eevee, 'volumetric_sample_distribution')
            if scene.eevee.use_volumetric_shadows:
                row.prop(scene.eevee, 'volumetric_shadow_samples')
    
    def invoke(self, context, event):
        wm = context.window_manager
        
        self.start = context.scene.camera.data.clip_start
        self.end = context.scene.camera.data.clip_end
        
        return wm.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(VolumetricsClipAdjust)


def unregister():
    bpy.utils.unregister_class(VolumetricsClipAdjust)


if __name__ == "__main__":
    register()

    # test call
    # bpy.ops.scene.eevee_volumetric_range()
