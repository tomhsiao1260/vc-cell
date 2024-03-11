import os
import tifffile
from core.MeshBVH import MeshBVH
from core.utils.cut import cut_obj, re_index
from core.utils.loader import parse_obj, save_obj
from utils.sdf import calculateSDF
from utils.draw import drawImage, drawBoxes
from utils.volume import getVolume

def cut(segmentID, layer, gap):
    path = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    data = parse_obj(path)

    data = cut_obj(data, layer, gap)
    re_index(data)
    save_obj(os.path.join('model', f'{segmentID}.obj'), data, materialName = segmentID)

def calCell(boundingData):
    boxMin = boundingData[:3]
    boxMax = boundingData[3:]

    lower = (boxMin // 500 + 1).astype('int')
    upper = (boxMax // 500 + 1).astype('int')

    for x in range(lower[0], upper[0] + 1):
        for y in range(lower[1], upper[1] + 1):
            for z in range(lower[2], upper[2] + 1):
                name = 'cell_yxz_{:03d}_{:03d}_{:03d}.tif'.format(y, x, z)
                path = os.path.join('../full-scrolls/Scroll1.volpkg/volume_grids/20230205180739', name)
                data = tifffile.imread(path)
                
                # z y x (1~100 layers)
                tifffile.imwrite(name, data[:20, :100, :50])

if __name__ == "__main__":
    # cut(segmentID = '20230702185753', layer = 1000, gap = 50)

    # path = os.path.join('model', 'plane.obj')
    path = os.path.join('model', '20230702185753.obj')

    data = parse_obj(path)
    bvh = MeshBVH(data)

    node = bvh._roots[0].left.left.left.left
    # points, indices, distances = calculateSDF(bvh, node)

    calCell(node.boundingData)

    # drawImage()
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)
