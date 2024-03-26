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

def save_n(data, data2, node, depth):
    d_list = []
    uv_list = []

    save_node(data, data2, node, depth, '', d_list, uv_list)

    d = np.concatenate(d_list, axis=0)
    uv = np.concatenate(uv_list, axis=0)

    return d, uv

def save_node(data, data2, node, depth, name, d_list, uv_list):
    depth -= 1

    leftNode = node.left
    rightNode = node.right

    leftName = name + '0'
    rightName = name + '1'

    leftData2 = cut_box(data2, leftNode.boundingData)
    rightData2 = cut_box(data2, rightNode.boundingData)

    if (depth == 0):
        left_data = cut_node(data, leftNode)
        # save_obj(f'{ leftName }.obj', left_data)
        # save_obj(f'{ leftName }_.obj', leftData2)
        d_left = d_cal(left_data, leftData2)
        uv_left = left_data['uvs']
        d_list.append(d_left)
        uv_list.append(uv_left)

        right_data = cut_node(data, rightNode)
        # save_obj(f'{ rightName }.obj', right_data)
        # save_obj(f'{ rightName }_.obj', rightData2)
        d_right = d_cal(right_data, rightData2)
        uv_right = right_data['uvs']
        d_list.append(d_right)
        uv_list.append(uv_right)
    else:
        save_node(data, leftData2, leftNode, depth, leftName, d_list, uv_list)
        save_node(data, rightData2, rightNode, depth, rightName, d_list, uv_list)

def d_cal(data_1, data_2):
    point = data_1['vertices']

    n, _ = point.shape  
    closestPoint = np.full((n, 3), 0)
    closestPointIndex = np.full((n), 0)
    closestDistance = np.full((n), float('inf'))

    triVertices = data_2['vertices'][data_2['faces'][:,:,0] - 1]
    tri = Triangle(triVertices)

    for i in range(triVertices.shape[0]):
        target = tri.closestPointToPointGPU(point, i)
        d = np.linalg.norm(point - target, axis=1)
        closestDistance = np.minimum(closestDistance, d)
        closestPoint = np.where((closestDistance == d)[..., np.newaxis], target, closestPoint)

    return closestDistance

path_1 = '../full-scrolls/Scroll1.volpkg/paths/20231012184424/20231012184423.obj'
path_2 = '../full-scrolls/Scroll1.volpkg/paths/20231012184424/20231012184424.obj'

data_1 = parse_obj('cut_1.obj')
data_2 = parse_obj('cut_2.obj')

bvh = MeshBVH(data_1)

data = bvh.data
data2 = data_2

node = bvh._roots[0]
d, uv = save_n(data, data2, node, depth=5)

w, h = 100, 100
image = np.zeros((h, w, 3), dtype=np.uint8)
color = (255, 255, 255)

# d_max = np.max(d)

# cv2.imshow('distance', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



