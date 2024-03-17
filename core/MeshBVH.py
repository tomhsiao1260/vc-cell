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

    def closestPointToPointGPU(self, point, offset, count, layer):
        w, h, _ = point.shape    
        closestPoint = np.full((w, h, 3), 0)
        closestPointIndex = np.full((w, h), 0)
        closestDistance = np.full((w, h), float('inf'))

        gap = 30
        triIndices = self.data['faces'][offset: offset + count]
        triangles = self.data['vertices'][triIndices[:,:,0] - 1]
        lowerBound = triangles[:,0,2] > (layer - gap)
        upperBound = triangles[:,0,2] < (layer + gap)
        mask = np.logical_and(lowerBound, upperBound)
        index = np.nonzero(mask)[0] + offset
        triangles = triangles[mask]
        tri = Triangle(triangles)

        for i in range(triangles.shape[0]):
            target = tri.closestPointToPointGPU(point, i)
            d = np.linalg.norm(point - target, axis=2)
            closestDistance = np.minimum(closestDistance, d)
            closestPoint = np.where((closestDistance == d)[:, :, np.newaxis], target, closestPoint)
            closestPointIndex = np.where((closestDistance == d), index[i], closestPointIndex)

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

