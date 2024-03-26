import cv2
import copy
import numpy as np
from core.utils.loader import parse_obj, save_obj
from core.utils.cut import cutLayer, cutBounding, re_index
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle

def cut_node(data, node):
    offset = node._offset
    count = node._count

    data_copy = copy.deepcopy(data)
    data_copy['faces'] = data_copy['faces'][offset : offset + count]
    re_index(data_copy)

    return data_copy

def cut_box(data, boundingData):
    boxMin = boundingData[:3]
    boxMax = boundingData[3:]

    data_copy = copy.deepcopy(data)
    cutBounding(data_copy, boxMin, boxMax)

    return data_copy


def save_node(data, data2, node, depth, name = ''):
    depth -= 1

    leftNode = node.left
    rightNode = node.right

    leftName = name + '0'
    rightName = name + '1'

    leftData2 = cut_box(data2, leftNode.boundingData)
    rightData2 = cut_box(data2, rightNode.boundingData)

    if (depth == 0):
        cut_data = cut_node(data, leftNode)
        save_obj(f'{ leftName }.obj', cut_data)
        save_obj(f'{ leftName }_.obj', leftData2)

        cut_data = cut_node(data, rightNode)
        save_obj(f'{ rightName }.obj', cut_data)
        save_obj(f'{ rightName }_.obj', rightData2)
    else:
        save_node(data, leftData2, leftNode, depth, leftName)
        save_node(data, rightData2, rightNode, depth, rightName)

path_1 = '../full-scrolls/Scroll1.volpkg/paths/20231012184424/20231012184423.obj'
path_2 = '../full-scrolls/Scroll1.volpkg/paths/20231012184424/20231012184424.obj'

# data = parse_obj(path_2)
# cutBounding(data, boxMin, boxMax)
# save_obj('cut_2.obj', data)

data_1 = parse_obj('cut_1.obj')
data_2 = parse_obj('cut_2.obj')

bvh = MeshBVH(data_1)

data = bvh.data
data2 = data_2
node = bvh._roots[0]
save_node(data, data2, node, depth=5)

# data_1 = parse_obj('cut_crunk_1.obj')
# data_2 = parse_obj('cut_crunk_2.obj')

# point = data_1['vertices']

# n, _ = point.shape  
# closestPoint = np.full((n, 3), 0)
# closestPointIndex = np.full((n), 0)
# closestDistance = np.full((n), float('inf'))

# triVertices = data_2['vertices'][data_2['faces'][:,:,0] - 1]
# tri = Triangle(triVertices)

# for i in range(triVertices.shape[0]):
#     target = tri.closestPointToPointGPU(point, i)
#     d = np.linalg.norm(point - target, axis=1)
#     closestDistance = np.minimum(closestDistance, d)
#     closestPoint = np.where((closestDistance == d)[:, np.newaxis], target, closestPoint)
#     closestPointIndex = np.where((closestDistance == d), index[i], closestPointIndex)

# print(closestDistance)

# w, h = 100, 100
# image = np.zeros((h, w, 3), dtype=np.uint8)
# color = (255, 255, 255)

# cv2.imshow('distance', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# cutBounding(data_1, boxMin, boxMax)
# cutBounding(data_2, boxMin, boxMax)


