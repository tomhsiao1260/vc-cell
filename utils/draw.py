import os
import cv2
import tifffile
import numpy as np
from core.objects.MeshBVHHelper import MeshBVHHelper

# def drawImage(path):
#     layerMin = 935
#     layerMax = 1065

#     for layer in range(layerMin, layerMax, 1):
#         image = cv2.imread(f'model/20230702185753/{layer}.png')

#         cv2.imshow('Distance', image)
#         # cv2.waitKey(0)
#         cv2.waitKey(10)
#         cv2.destroyAllWindows()

def drawImage(path):
    data = tifffile.imread(path)

    for layer in range(data.shape[0]):
        image = data[layer, :, :]

        cv2.imshow('Volume', image)
        # cv2.waitKey(0)
        cv2.waitKey(10)
        cv2.destroyAllWindows()

# def drawLabels(bvh, closestPointIndex, node = None):
#     if (node is None): node = bvh._roots[0]
#     boxMin = node.boundingData[:3]
#     boxMax = node.boundingData[3:]
#     windowSize = 1.0 * (boxMax - boxMin)
#     imgSize = (500, int(500 * windowSize[1] / windowSize[0]))

#     labels = cv2.imread(os.path.join('model', '20230702185753_inklabels.png'), cv2.IMREAD_UNCHANGED)

#     h_label, w_label = labels.shape
#     uv = data['uvs'][closestPointIndex]
#     x = (uv[:, :, 0] * (w_label - 1)).astype(int)
#     y = ((1 - uv[:, :, 1]) * (h_label - 1)).astype(int)

#     canvas = labels[y, x].transpose(1, 0).astype(np.uint8)
#     # canvas = p.transpose(1, 0, 2).astype(np.uint8)
#     canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
#     canvas = cv2.resize(canvas, imgSize)

#     cv2.imshow('Label', canvas)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

def drawBoxes(bvh):
    vertices = bvh.data['vertices']
    center = np.mean(vertices, axis=0)
    boxMin = np.min(vertices, axis=0)
    boxMax = np.max(vertices, axis=0)
    windowSize = 2 * np.max(np.maximum(boxMin - center, boxMax - center))
    windowSize = int(1.5 * windowSize)

    depth = 0
    helper = MeshBVHHelper(bvh)

    while (True):
        if (helper.draw(center, windowSize, depth)): depth += 1
        else: break