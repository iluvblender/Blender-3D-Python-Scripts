from typing import List

import bpy
from mathutils import Vector


BoundingBoxCoordinates = List[Vector]


class CoordinateExtents:
    def __init__(self, min, max):
        self._min = min
        self._max = max

    @property
    def min(self):
        return self._min
    
    @property
    def max(self):
        return self._max
    
    @classmethod
    def create_from(cls, dims):
        extent = cls(min(dims), max(dims))
        return extent

    def __repr__(self):
        return "<{0}> ({1}, {2})".format(self.__class__.__name__, self.min, self.max)


def make_bounding_box(x: CoordinateExtents, 
                      y: CoordinateExtents, 
                      z: CoordinateExtents) -> BoundingBoxCoordinates:
    
    pairs_xyz = (
        (x.min, y.min, z.min),
        (x.min, y.min, z.max),
        (x.min, y.max, z.max),
        (x.min, y.max, z.min),
        (x.max, y.min, z.min),
        (x.max, y.min, z.max),
        (x.max, y.max, z.max),
        (x.max, y.max, z.min),
    )

#    coords = tuple(map(Vector, pairs_xyz))
    coords = pairs_xyz
    return coords
    

"""
bbox_utils = D.texts['bbox_utils.py'].as_module()

ao = bpy.context.active_object
mesh = ao.data

vertices = map(lambda vtx: ao.matrix_world @ vtx.co, mesh.vertices)
xs, ys, zs = zip(*vertices)

extent_x = bbox_utils.CoordinateExtents.create_from(xs)
extent_y = bbox_utils.CoordinateExtents.create_from(ys)
extent_z = bbox_utils.CoordinateExtents.create_from(zs)

points = bbox_utils.make_bounding_box(extent_x, extent_y, extent_z)
for index, point in enumerate(points):
    exec("bb_{0} = Vector(point)".format(index))

del point
del index
del points
"""
