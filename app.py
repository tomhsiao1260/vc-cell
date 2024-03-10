import os
import cv2
import shutil
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

def drawDistaneField(bvh, node = None):
    path = os.path.join('model', '20230702185753')
    if not os.path.exists(path): os.makedirs(path)

    if (node is None): node = bvh._roots[0]
    boxMin = node.boundingData[:3]
    boxMax = node.boundingData[3:]
    layerMin = int(boxMin[2])
    # layerMax = int(boxMin[2]) + 1
    layerMax = int(boxMax[2])
    center = (boxMin + boxMax) / 2

    sampling = (1.0 * (boxMax - boxMin)).astype('int')
    windowSize = 1.0 * (boxMax - boxMin)
    maxDistance = np.max(windowSize[:2])
    # imgSize = (sampling[0], sampling[1])

    i, j = np.meshgrid(np.arange(sampling[0]), np.arange(sampling[1]), indexing='ij')

    for layer in range(layerMin, layerMax, 1):
        x = center[0] - windowSize[0] / 2 + (i + 0.5) * windowSize[0] / sampling[0]
        y = center[1] - windowSize[1] / 2 + (j + 0.5) * windowSize[1] / sampling[1]
        z = layer * np.full_like(x, 1)
        p = np.stack((x, y, z), axis=-1)

        closestPoint, closestPointIndex, closestDistance = bvh.closestPointToPointGPU(p, node._offset, node._count, layer)
        d = 255 * closestDistance / maxDistance

        canvas = d.transpose(1, 0).astype(np.uint8)
        # canvas = cv2.resize(canvas, imgSize)

        cv2.imshow('Distance', canvas)
        # cv2.waitKey(0)
        cv2.waitKey(10)
        cv2.destroyAllWindows()

        cv2.imwrite(os.path.join(path, f'{layer}.png'), canvas)

    # Copy the generated files to the client folder
    shutil.copytree('model/20230702185753' , 'client/public/20230702185753', dirs_exist_ok=True)

    return closestPoint, closestPointIndex, closestDistance

def drawLabels(bvh, closestPointIndex, node = None):
    if (node is None): node = bvh._roots[0]
    boxMin = node.boundingData[:3]
    boxMax = node.boundingData[3:]
    windowSize = 1.0 * (boxMax - boxMin)
    imgSize = (500, int(500 * windowSize[1] / windowSize[0]))

    labels = cv2.imread(os.path.join('model', '20230702185753_inklabels.png'), cv2.IMREAD_UNCHANGED)

    h_label, w_label = labels.shape
    uv = data['uvs'][closestPointIndex]
    x = (uv[:, :, 0] * (w_label - 1)).astype(int)
    y = ((1 - uv[:, :, 1]) * (h_label - 1)).astype(int)

    canvas = labels[y, x].transpose(1, 0).astype(np.uint8)
    # canvas = p.transpose(1, 0, 2).astype(np.uint8)
    canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
    canvas = cv2.resize(canvas, imgSize)

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
    # cut(segmentID = '20230702185753', layer = 1000, gap = 50)

    # p0 = np.array([[[1, 1, 1], [2, 2, 2], [3, 3, 3]], [[4, 4, 4], [5, 5, 5], [6, 6, 6]], [[7, 7, 7], [8, 8, 8], [9, 9, 9]]])
    # p1 = np.array([[[0, 0, 0], [100, 100, 100], [3, 3, 3]], [[4, 4, 4], [5, 5, 5], [6, 6, 6]], [[7, 7, 7], [8, 8, 8], [9, 9, 9]]])
    # a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # b = np.array([4, 5, 6])
    # c = np.dot(a, b)
    # c = np.logical_and(np.logical_not(a), b)

    # path = os.path.join('model', 'plane.obj')
    path = os.path.join('model', '20230702185753.obj')

    data = parse_obj(path)
    bvh = MeshBVH(data)

    node = bvh._roots[0].left.left.left.left
    points, indices, distances = drawDistaneField(bvh, node)
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)
