import os
import nrrd
import shutil
import tifffile
import numpy as np

from core.MeshBVH import MeshBVH
from core.utils.cut import cutLayer, cutBounding
from core.utils.loader import parse_obj, save_obj
from utils.volume import calculateVolume
from utils.sdf import calculateSDF, calculateUV, calculateLabel
from utils.draw import drawImage, drawUV, drawBoxes

#####################################################
######## Extract volume in the bounding box #########
#####################################################
def getVolume(boxMin, boxMax, volumeGridPath):
    volumeStack = calculateVolume(boxMin, boxMax, volumeGridPath)
    volumeStack *= 255

    # z, y, x -> x, y, z
    nrrdStack = np.transpose(volumeStack, (2, 1, 0)).astype(np.uint8)
    nrrd.write('model/volume.nrrd', nrrdStack)
    shutil.copy('model/volume.nrrd', 'client/public')
    # z, y, x -> z, y, x
    imageStack = np.transpose(volumeStack, (0, 1, 2)).astype(np.uint8)
    tifffile.imwrite('model/volume.png', imageStack)
    # debug
    drawImage('model/volume.png')

    return volumeStack

#####################################################
############ Distance field calculation #############
#####################################################
def getSDF(data):
    pStack, iStack, dStack = calculateSDF(data)
    dStack *= 255

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(dStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/sdf.nrrd', nrrdStack)
    shutil.copy('model/sdf.nrrd' , 'client/public')
    # z, x, y -> z, y, x
    imageStack = np.transpose(dStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/sdf.png', imageStack)
    # debug
    drawImage('model/sdf.png')

    return pStack, iStack, dStack

#####################################################
############## Inklabels 3D mapping #################
#####################################################
def getLabel(data, pStack, iStack, path):
    indices = data['faces'][iStack][:, :, :, :, 0] - 1
    triUVs = data['uvs'][indices]
    triVertices = data['vertices'][indices]

    uvStack = calculateUV(pStack, triVertices, triUVs)
    labelStack = calculateLabel(path, uvStack)
    labelStack *= 255

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(labelStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/inklabels.nrrd', nrrdStack)
    shutil.copy('model/inklabels.nrrd' , 'client/public')
    # z, x, y -> z, y, x
    imageStack = np.transpose(labelStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/inklabels.png', imageStack)
    # debug
    drawImage('model/inklabels.png')

    return labelStack

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
    # data = parse_obj(segmentLayerPath)

    # bvh = MeshBVH(data)
    # node = bvh._roots[0].left.left.right.left
    # drawUV(bvh)
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)

    # boxMin = node.boundingData[:3]
    # boxMax = node.boundingData[3:]
    # boxMin = np.array([ 3223, 2241, 935 ])
    # boxMax = np.array([ 3410, 2390, 1061 ])

    # cutBounding(data, boxMin, boxMax)
    # save_obj(segmentBoundingPath, data, mtl = segmentID)

    # # extract volume
    # volumeGridPath = '../full-scrolls/Scroll1.volpkg/volume_grids/20230205180739'
    # getVolume(boxMin, boxMax, volumeGridPath)

    # extract sdf
    data = parse_obj(segmentBoundingPath)
    pStack, iStack, dStack = getSDF(data)

    # extract inklabels
    inklabelPath = 'model/SPOILER_20230702185753.png'
    getLabel(data, pStack, iStack, inklabelPath)



