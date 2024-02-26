import numpy as np 
from core.math.Triangle import Triangle
from core.build.buildTree import buildPackedTree
from core.cast.closestPointToPoint import closestPointToPoint
from core.utils.iterationUtils import iterateOverTriangles

class MeshBVH:
    def __init__(self, data):
        # self._root = buildPackedTree(data)
        self.data = data

    def closestPointToPoint(self, point, minThreshold = 0, maxThreshold = float('inf')):
        return closestPointToPoint(self, point, minThreshold, maxThreshold)
    
    def shapecast(self, callbacks):
        iterateFunc = iterateOverTriangles
        intersectsTriangle = callbacks['intersectsTriangle']

        triIndices = self.data['faces'][:, :, 0]
        triangles = self.data['vertices'][triIndices - 1]
        tri = Triangle(triangles)

        offset = 0
        count = triangles.shape[0]
        iterateFunc(offset, count, intersectsTriangle, tri)

