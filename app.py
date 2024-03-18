import os
import nrrd
import shutil
import tifffile
import numpy as np

from core.MeshBVH import MeshBVH
from core.utils.cut import cutLayer, cutBounding
from core.utils.loader import parse_obj, save_obj
from utils.volume import calculateVolume
from utils.draw import drawImage, drawUV, drawBoxes
from utils.sdf import calculateSDF, calculateUV, calculateLabel

if __name__ == "__main__":
    segmentID = '20230702185753'
    segmentPath = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    segmentLayerPath = os.path.join('model', f'{segmentID}.obj')
    segmentBoundingPath = os.path.join('model', f'{segmentID}_bounding.obj')

    #####################################################
    ########## Cut a given segment along z-axis #########
    #####################################################
    # data = parse_obj(segmentPath)
    # cutLayer(data, layerMin = 950, layerMax = 1050)
    # save_obj(segmentLayerPath, data, mtl = segmentID)

    #####################################################
    ###### Cut a given segment via a bounding box #######
    #####################################################
    # data = parse_obj(os.path.join('model', f'{segmentID}.obj'))
    boxMin = np.array([ 3223, 2241, 935])
    boxMax = np.array([ 3410, 2390, 1061 ])
    # cutBounding(data, boxMin, boxMax)
    # save_obj(segmentBoundingPath, data, mtl = segmentID)

    #####################################################
    ############ Distance field calculation #############
    #####################################################
    data = parse_obj(segmentBoundingPath)
    pStack, iStack, dStack = calculateSDF(data)

    dStack *= 255
    # z, x, y -> x, y, z
    nrrdStack = np.transpose(dStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/sdf.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(dStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/sdf.png', imageStack)
    # copy the generated files to the client folder
    shutil.copy('model/sdf.nrrd' , 'client/public')

    #####################################################
    ############## Inklabels 3D mapping #################
    #####################################################
    indices = data['faces'][iStack][:, :, :, :, 0] - 1
    triUVs = data['uvs'][indices]
    triVertices = data['vertices'][indices]
    uvStack = calculateUV(pStack, triVertices, triUVs)
    labelStack = calculateLabel('model/SPOILER_20230702185753.png', uvStack)

    labelStack *= 255
    # z, x, y -> x, y, z
    nrrdStack = np.transpose(labelStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/inklabels.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(labelStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/inklabels.png', imageStack)
    # copy the generated files to the client folder
    shutil.copy('model/inklabels.nrrd' , 'client/public')

    # bvh = MeshBVH(data)
    # node = bvh._roots[0].left.left.left.left

    # calculateSDF(bvh, node)
    # calculateVolume(node.boundingData)

    # drawUV(bvh)
    # drawImage('model/volume.png')
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)



