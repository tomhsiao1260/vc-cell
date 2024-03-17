import os
import cv2
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
    # layerMin = int(boxMin[2]) + 50
    layerMin = int(boxMin[2])
    # layerMax = int(boxMin[2]) + 52
    layerMax = int(boxMax[2])
    center = (boxMin + boxMax) / 2

    sampling = (1.0 * (boxMax - boxMin)).astype('int')
    windowSize = 1.0 * (boxMax - boxMin)
    maxDistance = np.max(windowSize[:2])

    dStack = []
    indexStack = []
    pointStack = []

    i, j = np.meshgrid(np.arange(sampling[0]), np.arange(sampling[1]), indexing='ij')

    for layer in tqdm(range(layerMin, layerMax, 1)):
        x = center[0] - windowSize[0] / 2 + (i + 0.5) * windowSize[0] / sampling[0]
        y = center[1] - windowSize[1] / 2 + (j + 0.5) * windowSize[1] / sampling[1]
        z = layer * np.full_like(x, 1)
        p = np.stack((x, y, z), axis=-1)

        closestPoint, closestPointIndex, closestDistance = bvh.closestPointToPointGPU(p, node._offset, node._count, layer)
        d = 255 * closestDistance / maxDistance
        indexStack.append(closestPointIndex)
        pointStack.append(closestPoint)
        dStack.append(d)

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(np.array(dStack), (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/sdf.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(np.array(dStack), (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/sdf.png', imageStack)

    # Copy the generated files to the client folder
    shutil.copy('model/sdf.nrrd' , 'client/public')

    indices = np.array(indexStack)
    point = np.array(pointStack)
    indices = bvh.data['faces'][indices][:, :, :, :, 0] - 1

    triUVs = bvh.data['uvs'][indices]
    triVertices = bvh.data['vertices'][indices]
    uvStack = calculateUV(point, triVertices, triUVs)

    image = cv2.imread('model/SPOILER_20230702185753.png')
    h, w = image.shape[:2]

    inklabelStack = image[((1-uvStack[:, :, :, 1]) * h).astype(int), (uvStack[:, :, :, 0] * w).astype(int)][:,:,:,0]

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(np.array(inklabelStack), (1, 2, 0)).astype(np.uint8)
    nrrd.write('model/inklabels.nrrd', nrrdStack)
    # z, x, y -> z, y, x
    imageStack = np.transpose(np.array(inklabelStack), (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('model/inklabels.png', imageStack)

    # Copy the generated files to the client folder
    shutil.copy('model/inklabels.nrrd' , 'client/public')

# UV Interpolation
def calculateUV(point, triVertices, triUVs):
    d = np.linalg.norm(triVertices - point[:, :, :, np.newaxis, :], axis=-1)
    d += 1e-5
    d = 1 / d
    d = d / np.sum(d, axis=-1)[:, :, :, np.newaxis]

    uvStack = np.sum(triUVs * d[..., np.newaxis], axis=-2)
    # uvStack = triUVs[:, :, :, 0]
    
    return uvStack
