import os
import cv2
import numpy as np
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle
from core.objects.MeshBVHHelper import MeshBVHHelper
from core.utils.loader import parse_obj

def drawDistaneField(bvh, center, windowSize, data):
    imgSize = 500
    canvas = np.zeros((imgSize, imgSize, 3), dtype=np.uint8)

    labels = cv2.imread(os.path.join('model', '20230702185753_inklabels.png'), cv2.IMREAD_UNCHANGED)
    h_labels, w_labels = labels.shape

    sampling = 50
    layer = center[2]
    gap = windowSize / sampling
    igap = imgSize / sampling
    maxDistance = windowSize / 2

    triIndices = data['faces'][:, :, 0]
    triangles = data['vertices'][triIndices - 1]
    triUV = data['uvs'][triIndices - 1]

    for i in range(sampling):
        for j in range(sampling):
            x = center[0] - windowSize / 2 + (i + 0.5) * gap
            y = center[1] - windowSize / 2 + (j + 0.5) * gap
            p = np.array([x, y, layer])
            point, distance, faceIndex = bvh.closestPointToPoint(p)

            d = np.linalg.norm(triangles[faceIndex] - np.array([0, 0, 1]), axis=1)
            d = np.maximum(d, 0.0001)
            weights = 1 / d
            weights /= np.sum(weights)
            uv_mean = np.sum(triUV[faceIndex] * weights[:, np.newaxis], axis=0)

            intensity = labels[int((1 - uv_mean[1]) * h_labels), int(uv_mean[0] * w_labels)]

            # normal_point = (point - center + windowSize / 2) / windowSize
            # canvas[j*int(igap):(j+1)*int(igap), i*int(igap):(i+1)*int(igap), 0] = 255
            # canvas[j*int(igap):(j+1)*int(igap), i*int(igap):(i+1)*int(igap), 1] = 255 * normal_point[1]
            # canvas[j*int(igap):(j+1)*int(igap), i*int(igap):(i+1)*int(igap), 2] = 255 * normal_point[0]

            canvas[j*int(igap):(j+1)*int(igap), i*int(igap):(i+1)*int(igap), 0] = intensity
            canvas[j*int(igap):(j+1)*int(igap), i*int(igap):(i+1)*int(igap), 1] = intensity
            canvas[j*int(igap):(j+1)*int(igap), i*int(igap):(i+1)*int(igap), 2] = intensity

            # canvas[j*int(igap):(j+1)*int(igap), i*int(igap):(i+1)*int(igap), :] = 255 * distance / maxDistance

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

    drawDistaneField(bvh, center, windowSize, data)

    # depth = 0
    # helper = MeshBVHHelper(bvh)

    # while (True):
    #     if (helper.draw(center, windowSize, depth)): depth += 1
    #     else: break
