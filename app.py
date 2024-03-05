import os
import cv2
import numpy as np
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle
from core.objects.MeshBVHHelper import MeshBVHHelper
from core.utils.cut import cut_obj, re_index
from core.utils.loader import parse_obj, save_obj

def cut(segmentID, layer, gap):
    path = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    data = parse_obj(path)

    data = cut_obj(data, layer, gap)
    re_index(data)
    save_obj(os.path.join('model', f'{segmentID}.obj'), data, materialName = segmentID)

def drawDistaneField(bvh):
    data = bvh.data
    center = np.mean(data['vertices'], axis=0)
    boxMin = np.min(data['vertices'], axis=0)
    boxMax = np.max(data['vertices'], axis=0)
    windowSize = 2 * np.max(np.maximum(boxMin - center, boxMax - center))
    windowSize = int(1.5 * windowSize)

    imgSize = 500
    sampling = 50
    layer = center[2]
    gap = windowSize / sampling
    maxDistance = windowSize / 2

    i, j = np.meshgrid(np.arange(sampling), np.arange(sampling), indexing='ij')
    x = center[0] - windowSize / 2 + (i + 0.5) * gap
    y = center[1] - windowSize / 2 + (j + 0.5) * gap
    z = layer * np.full_like(x, 1)
    p = np.stack((x, y, z), axis=-1)

    closestPoint, closestPointIndex, closestDistance = bvh.closestPointToPointGPU(p)
    d = 255 * closestDistance / maxDistance

    canvas = d.transpose(1, 0).astype(np.uint8)
    # canvas = p.transpose(1, 0, 2).astype(np.uint8)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
    canvas = cv2.resize(canvas, (imgSize, imgSize))

    cv2.imshow('Distance', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return closestPoint, closestPointIndex, closestDistance

def drawLabels(closestPointIndex):
    imgSize = 500
    labels = cv2.imread(os.path.join('model', '20230702185753_inklabels.png'), cv2.IMREAD_UNCHANGED)

    h_label, w_label = labels.shape
    uv = data['uvs'][closestPointIndex]
    x = (uv[:, :, 0] * (w_label - 1)).astype(int)
    y = ((1 - uv[:, :, 1]) * (h_label - 1)).astype(int)

    canvas = labels[y, x].transpose(1, 0).astype(np.uint8)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
    canvas = cv2.resize(canvas, (imgSize, imgSize))

    cv2.imshow('Label', canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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

if __name__ == "__main__":
    # cut(segmentID = '20230702185753', layer = 1000, gap = 10)

    # path = os.path.join('model', 'plane.obj')
    path = os.path.join('model', '20230702185753.obj')

    data = parse_obj(path)
    bvh = MeshBVH(data)

    _, closestPointIndex, _ = drawDistaneField(bvh)
    drawLabels(closestPointIndex)
    # drawBoxes(bvh)
