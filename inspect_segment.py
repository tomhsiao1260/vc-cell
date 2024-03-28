import os
import cv2
import copy
import json
import shutil
import argparse
import numpy as np
from core.utils.loader import parse_obj, save_obj
from core.utils.cut import cutLayer, cutDivide, cutBounding, re_index
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle

# cut OBJ into multi chunks along z-axis
def preprocess(data, folderName):
    layerMin = np.min(data['vertices'][:, 2])
    layerMax = np.max(data['vertices'][:, 2])

    layerMin = int(layerMin // 100) * 100
    layerMax = int(layerMax // 100) * 100
    gap = layerMax - layerMin

    if (gap <= 100):
        name = os.path.join(folderName, f'z{layerMin}_d{gap}.obj')
        save_obj(name, data)
    else:
        cutZ = int(((layerMin + layerMax) / 2) // 100) * 100
        left, right = cutDivide(data, cutZ)
        preprocess(left, folderName)
        preprocess(right, folderName)

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

    def cal(node, mode, name):
        if (mode == 'left'): name += '0'
        if (mode == 'right'): name += '1'
        
        c_data2 = cut_box(data2, node.boundingData)

        if (depth == 0):
            c_data = cut_node(data, node)
            # save_obj(f'{ name }.obj', c_data)
            # save_obj(f'{ name }_.obj', c_data2)
            c_d = d_cal(c_data, c_data2)
            c_uv = c_data['uvs']

            if not np.isinf(np.max(c_d)):
                d_list.append(c_d)
                uv_list.append(c_uv)
        else:
            save_node(data, c_data2, node, depth, name, d_list, uv_list)

    depth -= 1
    if hasattr(node, 'left'):
        cal(node.left, 'left', name)
    if hasattr(node, 'right'):
        cal(node.right, 'right', name)

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
        closestPointIndex = np.where((closestDistance == d), i, closestPointIndex)

    triNormals = data_2['normals'][data_2['faces'][:,:,0] - 1]
    nor = triNormals[closestPointIndex][:,0]
    dir = closestPoint - point

    t = np.sum(nor * dir, axis=1)
    sign = np.where(t < 0, -1, 1)
    closestDistance *= sign

    return closestDistance

def draw(d, uv):
    d_max = 10
    # d_max = np.max(np.abs(d))
    dotSize = 3
    d = d / d_max

    # h, w = 500, 500
    h, w = 1575, 2336
    # h, w = 15751, 23356
    image = np.zeros((h, w, 3), dtype=np.uint8)

    for depth, uv in zip(d, uv):
        u, v = uv
        u = int(w * u)
        v = int(h * (1-v))

        value = min(255 * abs(depth), 255)

        if depth > 0: color = (0, 0, value)
        if not depth > 0: color = (0, value, 0)
        # color = (value, value, value)
        cv2.circle(image, (u, v), dotSize, color, -1)

    cv2.imshow('distance', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('d.png', image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Segmentation inspection / evaluation')
    parser.add_argument('--mode', type=str, help='preprocess or inspection')
    parser.add_argument('--name', type=str, help='output folder name')
    parser.add_argument('--path', type=str, help='segment OBJ path')
    args = parser.parse_args()

    # cut the segment
    if (args.mode == 'preprocess'):
        folderName = os.path.join('output', args.name)
        shutil.rmtree(folderName, ignore_errors=True)
        os.makedirs(folderName)
        
        data = parse_obj(args.path)
        preprocess(data, folderName)

# path = '../full-scrolls/Scroll1.volpkg/paths/20231012184424/20231012184424.obj'
# path = '../full-scrolls/Scroll1.volpkg/paths/20231012184424/20231012184423.obj'

# d = []
# uv = []

# for i in range(0, 2000, 100):
# # for i in range(0, 13300, 100):
#     print(f'processing {i} ...')

#     name = f'{i}_100.obj'
#     data_1 = parse_obj(os.path.join('output', '20231012184423', name))
#     data_2 = parse_obj(os.path.join('output', '20231012184424', name))

#     bvh = MeshBVH(data_1)
#     data = bvh.data

#     node = bvh._roots[0]
#     sub_d, sub_uv = save_n(data, data_2, node, depth=5)

#     d.append(sub_d)
#     uv.append(sub_uv)

# d = np.concatenate(d, axis=0)
# uv = np.concatenate(uv, axis=0)

# d = np.around(d, decimals=5)
# d_uv = np.column_stack((d, uv))

# meta = {}
# meta['d_uv'] = d_uv.tolist()

# # save main meta.json
# with open('output/meta.json', "w") as f:
#     json.dump(meta, f, indent=4)

# with open('output/meta.json', 'r') as f:
#     data = json.load(f)
#     data = np.array(data['d_uv'])

#     d = data[:, 0]
#     uv = data[:, 1:]

#     draw(d, uv)



