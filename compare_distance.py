import os
import cv2
import copy
import shutil
import numpy as np
from core.utils.loader import parse_obj, save_obj
from core.utils.cut import cutLayer, cutDivide, cutBounding, re_index
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

        right_data = cut_node(data, rightNode)
        # save_obj(f'{ rightName }.obj', right_data)
        # save_obj(f'{ rightName }_.obj', rightData2)
        d_right = d_cal(right_data, rightData2)
        uv_right = right_data['uvs']

        if not np.isinf(np.max(d_left)):
            d_list.append(d_left)
            uv_list.append(uv_left)

        if not np.isinf(np.max(d_right)):
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

def save_layer(data, id):
    layerMin = np.min(data['vertices'][:, 2])
    layerMax = np.max(data['vertices'][:, 2])

    layerMin = int(layerMin // 100) * 100
    layerMax = int(layerMax // 100) * 100
    gap = layerMax - layerMin

    if (gap <= 100):
        name = os.path.join('output', id, f'{layerMin}_{gap}.obj')
        save_obj(name, data)
    else:
        cutZ = int(((layerMin + layerMax) / 2) // 100) * 100
        left, right = cutDivide(data, cutZ)
        save_layer(left, id)
        save_layer(right, id)

# id = '20231012184423'
id = '20231012184424'

# path = os.path.join('../full-scrolls/Scroll1.volpkg/paths', '20231012184424', id + '.obj')

# # clear output folder
# folder = os.path.join('output', id)
# shutil.rmtree(folder, ignore_errors=True)
# if not os.path.exists(folder): os.makedirs(folder)

# data = parse_obj(path)
# save_layer(data, id)

# w, h = 500, 500
# image = np.zeros((h, w, 3), dtype=np.uint8)

image = cv2.imread('d.png')
h, w = image.shape[:2]

for i in range(0, 2000, 100):
# for i in range(0, 13300, 100):
    print(f'processing {i} ...')

    name = f'{i}_100.obj'
    data_1 = parse_obj(os.path.join('output', '20231012184423', name))
    data_2 = parse_obj(os.path.join('output', '20231012184424', name))

    bvh = MeshBVH(data_1)
    data = bvh.data

    node = bvh._roots[0]
    d, uv = save_n(data, data_2, node, depth=5)
    d_max = np.max(d)

    for depth, uv in zip(d, uv):
        u, v = uv

        u = int(w * u)
        v = int(h * (1-v))

        value = 255 * depth / d_max
        color = (value, value, value)
        cv2.circle(image, (u, v), 1, color, -1)

cv2.imshow('distance', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('d.png', image)



