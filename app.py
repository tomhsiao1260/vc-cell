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

    p = np.array([-1, -1, 3])
    # p = np.array([-1, 0.5, -3])
    # p = np.array([0, 2, 3])
    # p = np.array([1, 1, -3])
    # p = np.array([2, 0, 3])
    # p = np.array([0.5, -2, -3])
    # p = np.array([0.5, 0.5, 3])

    point, distance, faceIndex = bvh.closestPointToPoint(p)
    print('faceIndex: ', faceIndex)
    print('point: ', point)
    print('distance: ', distance)

    helper = MeshBVHHelper(bvh)
    helper.draw(depth = 0)
    helper.draw(depth = 1)
    helper.draw(depth = 2)
