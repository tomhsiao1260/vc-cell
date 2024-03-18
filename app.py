import os
import numpy as np
from core.MeshBVH import MeshBVH
from core.utils.cut import cutLayer, cutBounding
from core.utils.loader import parse_obj, save_obj
from utils.sdf import calculateSDF, calSDF
from utils.draw import drawImage, drawUV, drawBoxes
from utils.volume import calculateVolume

import nrrd
import tifffile
import shutil

if __name__ == "__main__":
    segmentID = '20230702185753'
    segmentPath = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    segmentLayerPath = os.path.join('model', f'{segmentID}.obj')
    segmentBoundingPath = os.path.join('model', f'{segmentID}_bounding.obj')

    # # cut a given segment along z-axis
    # data = parse_obj(segmentPath)
    # cutLayer(data, layerMin = 950, layerMax = 1050)
    # save_obj(segmentLayerPath, data, mtl = segmentID)

    # # cut a given segment via a bounding box
    # data = parse_obj(os.path.join('model', f'{segmentID}.obj'))
    # boxMin = np.array([ 3223, 2241, 935])
    # boxMax = np.array([ 3410, 2390, 1061 ])
    # cutBounding(data, boxMin, boxMax)
    # save_obj(segmentBoundingPath, data, mtl = segmentID)

    data = parse_obj(segmentBoundingPath)
    dStack, inklabelStack = calSDF(data)
    dStack *= 255
    inklabelStack *= 255

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(dStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/sdf.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(dStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/sdf.png', imageStack)
    # Copy the generated files to the client folder
    shutil.copy('model/sdf.nrrd' , 'client/public')

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(inklabelStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/inklabels.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(inklabelStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/inklabels.png', imageStack)
    # Copy the generated files to the client folder
    shutil.copy('model/inklabels.nrrd' , 'client/public')

    # bvh = MeshBVH(data)
    # node = bvh._roots[0].left.left.left.left

    # calculateSDF(bvh, node)
    # calculateVolume(node.boundingData)

    # drawUV(bvh)
    # drawImage('model/volume.png')
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)



