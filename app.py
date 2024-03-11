import os
from core.MeshBVH import MeshBVH
from core.utils.cut import cut_obj, re_index
from core.utils.loader import parse_obj, save_obj
from utils.sdf import calculateSDF
from utils.draw import drawImage, drawBoxes
from utils.volume import calculateVolume

def cut(segmentID, layer, gap):
    path = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    data = parse_obj(path)

    data = cut_obj(data, layer, gap)
    re_index(data)
    save_obj(os.path.join('model', f'{segmentID}.obj'), data, materialName = segmentID)

if __name__ == "__main__":
    # cut(segmentID = '20230702185753', layer = 1000, gap = 50)

    # path = os.path.join('model', 'plane.obj')
    path = os.path.join('model', '20230702185753.obj')

    data = parse_obj(path)
    bvh = MeshBVH(data)

    node = bvh._roots[0].left.left.left.left
    # points, indices, distances = calculateSDF(bvh, node)

    calculateVolume(node.boundingData)

    # drawImage()
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)
