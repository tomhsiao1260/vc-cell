import os
import cv2
import numpy as np
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle
from core.objects.MeshBVHHelper import MeshBVHHelper
from core.utils.loader import parse_obj

def drawDistaneField(bvh, center, windowSize):
    imgSize = 500
    canvas = np.zeros((imgSize, imgSize, 3), dtype=np.uint8)

    sampling = 50
    layer = center[2]
    gap = windowSize / sampling
    igap = imgSize / sampling
    maxDistance = windowSize / 2

    for i in range(sampling):
        for j in range(sampling):
            x = center[0] - windowSize / 2 + (i + 0.5) * gap
            y = center[1] - windowSize / 2 + (j + 0.5) * gap
            p = np.array([x, y, layer])
            point, distance, faceIndex = bvh.closestPointToPoint(p)

            canvas[int(j*igap):int((j+1)*igap), int(i*igap):int((i+1)*igap), :] = 255 * distance / maxDistance

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
