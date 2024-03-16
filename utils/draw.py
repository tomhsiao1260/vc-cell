import os
import cv2
import tifffile
import numpy as np
from core.objects.MeshBVHHelper import MeshBVHHelper

def drawImage(path):
    data = tifffile.imread(path)

    for layer in range(data.shape[0]):
        image = data[layer, :, :]

        cv2.imshow('Volume', image)
        # cv2.waitKey(0)
        cv2.waitKey(10)
        cv2.destroyAllWindows()

def drawUV(bvh):
    w, h = 869, 675
    image = np.zeros((h, w, 3), dtype=np.uint8)

    drawUVNode(image, bvh, bvh._roots[0].left, color = (255, 0, 0))
    drawUVNode(image, bvh, bvh._roots[0].right, color = (0, 255, 0))

    cv2.imshow('UV', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def drawUVNode(image, bvh, node, color = (255, 255, 255)):
    h, w, _ = image.shape
    offset = node._offset
    count = node._count

    triIndices = bvh.data['faces'][offset: offset + count]
    triUVs = bvh.data['uvs'][triIndices[:,:,0] - 1]

    triUVs[:, :, 0] *= w
    triUVs[:, :, 1] *= h
    triUVs = triUVs.astype(int)

    for tri in triUVs:
        cv2.line(image, tuple(tri[0]), tuple(tri[1]), color, 1)
        cv2.line(image, tuple(tri[1]), tuple(tri[2]), color, 1)
        cv2.line(image, tuple(tri[2]), tuple(tri[0]), color, 1)


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