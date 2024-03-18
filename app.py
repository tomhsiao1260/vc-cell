import os
import numpy as np
from core.MeshBVH import MeshBVH
from core.utils.cut import cut_obj, re_index
from core.utils.loader import parse_obj, save_obj
from utils.sdf import calculateSDF
from utils.draw import drawImage, drawUV, drawBoxes
from utils.volume import calculateVolume

def cutLayer(segmentID, layerMin, layerMax):
    path = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    data = parse_obj(path)

    # cut z
    cut_obj(data, splitAxis = 2, splitOffset = layerMin, survive = 'right')
    cut_obj(data, splitAxis = 2, splitOffset = layerMax, survive = 'left')

    re_index(data)
    save_obj(os.path.join('model', f'{segmentID}.obj'), data, mtl = segmentID)

def cutBounding(path, boundingData):
    data = parse_obj(path)
    boxMin = boundingData[:3]
    boxMax = boundingData[3:]

    # cut x
    cut_obj(data, splitAxis = 0, splitOffset = boxMin[0], survive = 'right')
    cut_obj(data, splitAxis = 0, splitOffset = boxMax[0], survive = 'left')
    # cut y
    cut_obj(data, splitAxis = 1, splitOffset = boxMin[1], survive = 'right')
    cut_obj(data, splitAxis = 1, splitOffset = boxMax[1], survive = 'left')
    # cut z
    cut_obj(data, splitAxis = 2, splitOffset = boxMin[2], survive = 'right')
    cut_obj(data, splitAxis = 2, splitOffset = boxMax[2], survive = 'left')

    re_index(data)

    segmentID = '20230702185753'
    save_obj(os.path.join('model', 'ok.obj'), data, mtl = segmentID)

if __name__ == "__main__":
    cutLayer(segmentID = '20230702185753', layerMin = 950, layerMax = 1050)

    # path = os.path.join('model', 'plane.obj')
    # path = os.path.join('model', '20230702185753.obj')

    # data = parse_obj(path)
    # bvh = MeshBVH(data)

    # node = bvh._roots[0].left.left.left.left
    # boundingData = np.array([ 3223.82, 2241.01, 935.42, 3410.5, 2390.79, 1061.63 ])

    # cutBounding(path, boundingData)
    # calculateSDF(bvh, node)
    # calculateVolume(node.boundingData)

    # drawUV(bvh)
    # drawImage('model/volume.png')
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)



