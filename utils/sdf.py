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

    stack = []
    i, j = np.meshgrid(np.arange(sampling[0]), np.arange(sampling[1]), indexing='ij')

    for layer in tqdm(range(layerMin, layerMax, 1)):
        x = center[0] - windowSize[0] / 2 + (i + 0.5) * windowSize[0] / sampling[0]
        y = center[1] - windowSize[1] / 2 + (j + 0.5) * windowSize[1] / sampling[1]
        z = layer * np.full_like(x, 1)
        p = np.stack((x, y, z), axis=-1)

        closestPoint, closestPointIndex, closestDistance = bvh.closestPointToPointGPU(p, node._offset, node._count, layer)
        d = 255 * closestDistance / maxDistance
        stack.append(d)

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(np.array(stack).astype(np.uint8), (1, 2, 0))
    nrrd.write('model/sdf.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(np.array(stack).astype(np.uint8), (0, 2, 1))
    tifffile.imwrite('model/sdf.png', imageStack)

    # Copy the generated files to the client folder
    shutil.copy('model/sdf.nrrd' , 'client/public')

    return closestPoint, closestPointIndex, closestDistance
