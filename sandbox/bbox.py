import bpy
from mathutils import Vector

class LayoutObject:
    def __init__(self, obj):
        self.obj = obj
        self.bbox = None
        
        self._init_world_bbox()
    
    def _init_world_bbox(self):
        obj = self.obj
        self.bbox = tuple(
                        map(
                            lambda bbco: obj.matrix_world@Vector(bbco),
                            obj.bound_box
                            )
                        )

    def debug_bbco(self, env):
        for index, bbco in enumerate(self.bbox):
            env["bco{0}".format(index)] = bbco 

    
