import os
import nrrd
import shutil
import tifffile
import numpy as np
from tqdm import tqdm

def calculateSDF(bvh, node = None):
    # clear output folder
    path = os.path.join('model', '20230702185753')
    clientPath = os.path.join('client', 'public', '20230702185753')
    shutil.rmtree(path, ignore_errors=True)
    shutil.rmtree(clientPath, ignore_errors=True)
    if not os.path.exists(path): os.makedirs(path)
    if not os.path.exists(clientPath): os.makedirs(clientPath)

    if (node is None): node = bvh._roots[0]
    boxMin = node.boundingData[:3]
    boxMax = node.boundingData[3:]
    layerMin = int(boxMin[2])
    # layerMax = int(boxMin[2]) + 5
    layerMax = int(boxMax[2])
    center = (boxMin + boxMax) / 2

    sampling = (1.0 * (boxMax - boxMin)).astype('int')
    windowSize = 1.0 * (boxMax - boxMin)
    maxDistance = np.max(windowSize[:2])

    dStack = []
    indexStack = []
    i, j = np.meshgrid(np.arange(sampling[0]), np.arange(sampling[1]), indexing='ij')

    for layer in tqdm(range(layerMin, layerMax, 1)):
        x = center[0] - windowSize[0] / 2 + (i + 0.5) * windowSize[0] / sampling[0]
        y = center[1] - windowSize[1] / 2 + (j + 0.5) * windowSize[1] / sampling[1]
        z = layer * np.full_like(x, 1)
        p = np.stack((x, y, z), axis=-1)

        closestPoint, closestPointIndex, closestDistance = bvh.closestPointToPointGPU(p, node._offset, node._count, layer)
        d = 255 * closestDistance / maxDistance
        indexStack.append(closestPointIndex)
        dStack.append(d)

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(np.array(dStack), (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/sdf.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(np.array(dStack), (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/sdf.png', imageStack)

    # Copy the generated files to the client folder
    shutil.copy('model/sdf.nrrd' , 'client/public')

    uvStack = bvh.data['uvs'][np.array(indexStack)]
    uStack = 255 * uvStack[:, :, :, 0]
    vStack = 255 * uvStack[:, :, :, 1]

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(np.array(uStack), (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/u.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(np.array(uStack), (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/u.png', imageStack)

    # Copy the generated files to the client folder
    shutil.copy('model/u.nrrd' , 'client/public')

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(np.array(vStack), (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/v.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(np.array(vStack), (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/v.png', imageStack)

    # Copy the generated files to the client folder
    shutil.copy('model/v.nrrd' , 'client/public')
