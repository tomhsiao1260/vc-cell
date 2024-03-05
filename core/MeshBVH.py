import numpy as np 
from core.math.Triangle import Triangle
from core.build.buildTree import buildPackedTree
from core.cast.closestPointToPoint import closestPointToPoint
from core.utils.iterationUtils import iterateOverTriangles
from core.cast.shapecast import shapecast

class MeshBVH:
    def __init__(self, data):
        root = buildPackedTree(data)
        self.data = data
        self._roots = [root]

    def closestPointToPoint(self, point, minThreshold = 0, maxThreshold = float('inf')):
        return closestPointToPoint(self, point, minThreshold, maxThreshold)

    def closestPointToPointGPU(self, point):
        w, h, _ = point.shape
        vertices = self.data['vertices']

        closestPoint = np.full((w, h, 3), 0)
        closestPointIndex = np.full((w, h), 0)
        closestDistance = np.full((w, h), float('inf'))

        for i, target in enumerate(vertices):
            d = np.linalg.norm(point - target, axis=2)
            closestDistance = np.minimum(closestDistance, d)
            closestPoint[(closestDistance == d)] = target
            closestPointIndex[(closestDistance == d)] = i

        return closestPoint, closestPointIndex, closestDistance

    def shapecast(self, callbacks):
        boundsTraverseOrder = callbacks['boundsTraverseOrder']
        intersectsBounds = callbacks['intersectsBounds']
        intersectsTriangle = callbacks['intersectsTriangle']

        triIndices = self.data['faces'][:, :, 0]
        triangles = self.data['vertices'][triIndices - 1]
        tri = Triangle(triangles)

        def intersectsRange(offset, count):
            nonlocal intersectsTriangle, tri
            iterateOverTriangles(offset, count, intersectsTriangle, tri)

		# run shapecast
        result = False
        result = shapecast(
            self,
			intersectsBounds,
			intersectsRange,
			boundsTraverseOrder,
		)

        return result

