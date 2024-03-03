import os
import cv2
import numpy as np
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle
from core.objects.MeshBVHHelper import MeshBVHHelper
from core.utils.loader import parse_obj

def drawDistaneField(bvh, center, windowSize):
    imgSize = 500
    sampling = 50
    layer = center[2]
    gap = windowSize / sampling
    igap = imgSize / sampling
    maxDistance = windowSize / 2

    i, j = np.meshgrid(np.arange(sampling), np.arange(sampling), indexing='ij')
    x = center[0] - windowSize / 2 + (i + 0.5) * gap
    y = center[1] - windowSize / 2 + (j + 0.5) * gap
    z = layer * np.full_like(x, 1)
    p = np.stack((x, y, z), axis=-1)

    distance = bvh.closestPointToPointGPU(p, center)
    d = 255 * distance / maxDistance

    canvas = d.transpose(1, 0).astype(np.uint8)
    # canvas = p.transpose(1, 0, 2).astype(np.uint8)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
    canvas = cv2.resize(canvas, (imgSize, imgSize))

    cv2.imshow('Box', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # path = os.path.join('model', 'plane.obj')
    path = os.path.join('model', '20230702185753.obj')

    data = parse_obj(path)
    bvh = MeshBVH(data)

    center = np.mean(data['vertices'], axis=0)
    boxMin = np.min(data['vertices'], axis=0)
    boxMax = np.max(data['vertices'], axis=0)
    windowSize = 2 * np.max(np.maximum(boxMin - center, boxMax - center))
    windowSize = int(1.5 * windowSize)

    drawDistaneField(bvh, center, windowSize)

    # depth = 0
    # helper = MeshBVHHelper(bvh)

    # while (True):
    #     if (helper.draw(center, windowSize, depth)): depth += 1
    #     else: break
