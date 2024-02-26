import numpy as np 
from core.math.Triangle import Triangle
from core.build.buildTree import buildPackedTree
from core.cast.closestPointToPoint import closestPointToPoint

class MeshBVH:
    def __init__(self, data):
        self._root = buildPackedTree(data)

    def closestPointToPoint(self, point, minThreshold = 0, maxThreshold = float('inf')):
        return closestPointToPoint(self, point, minThreshold, maxThreshold)
    
    def shapecast(self, callbacks):
        tri = Triangle(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]]))
        intersectsTriangle = callbacks['intersectsTriangle']
        intersectsTriangle(tri, triIndex = 0)

