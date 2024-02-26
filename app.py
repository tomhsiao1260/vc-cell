import os
import numpy as np
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle
from core.objects.MeshBVHHelper import MeshBVHHelper
from core.utils.loader import parse_obj

if __name__ == "__main__":
    path = os.path.join('model', 'plane.obj')

    data = parse_obj(path)
    bvh = MeshBVH(data)

    helper = MeshBVHHelper(bvh)
    helper.draw()

    # tri = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    # T = Triangle(tri)

    # p1 = np.array([-1, -1, 3])
    # p2 = np.array([-1, 0.5, -3])
    # p3 = np.array([0, 2, 3])
    # p4 = np.array([1, 1, -3])
    # p5 = np.array([2, 0, 3])
    # p6 = np.array([0.5, -2, -3])
    # p7 = np.array([0.5, 0.5, 3])

    # print(T.closestPointToPoint(p1))
    # print(T.closestPointToPoint(p2))
    # print(T.closestPointToPoint(p3))
    # print(T.closestPointToPoint(p4))
    # print(T.closestPointToPoint(p5))
    # print(T.closestPointToPoint(p6))
    # print(T.closestPointToPoint(p7))

