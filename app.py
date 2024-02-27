import os
import cv2
import numpy as np
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle
from core.objects.MeshBVHHelper import MeshBVHHelper
from core.utils.loader import parse_obj

def drawDistaneField(bvh):
    g = 10
    w, h, d = 7, 7, 0.1
    hSampling, wSampling = 50, 50
    canvas = np.zeros((hSampling * g, wSampling * g, 3), dtype=np.uint8)
    maxDistance = np.sqrt(100)

    for i in range(hSampling + 1):
        for j in range(wSampling + 1):
            p = np.array([w * (j/wSampling - 0.5), h * (i/hSampling - 0.5), d])
            point, distance, faceIndex = bvh.closestPointToPoint(p)

            canvas[i*g:(i+1)*g, j*g:(j+1)*g, :] = 255 * distance / maxDistance
            
    cv2.imshow('Box', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

    # point, distance, faceIndex = bvh.closestPointToPoint(p)
    # print('faceIndex: ', faceIndex)
    # print('point: ', point)
    # print('distance: ', distance)

    drawDistaneField(bvh)

    # helper = MeshBVHHelper(bvh)
    # helper.draw(depth = 0)
    # helper.draw(depth = 1)
    # helper.draw(depth = 2)
