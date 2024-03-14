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
    # layerMin = int(boxMin[2]) + 50
    layerMin = int(boxMin[2])
    # layerMax = int(boxMin[2]) + 55
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
    # indices = bvh.data['faces'][indices][:, :, :, 0, 0] - 1

    triUVs = bvh.data['uvs'][indices]
    triVertices = bvh.data['vertices'][indices]
    uvStack = calUV(point, triVertices, triUVs)

    uStack = 255 * uvStack[:, :, :, 0]
    vStack = 255 * uvStack[:, :, :, 1]
    # uStack = 255 * (uStack - np.min(uStack)) / (np.max(uStack) - np.min(uStack))
    # vStack = 255 * (vStack - np.min(vStack)) / (np.max(vStack) - np.min(vStack))

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

# bi-linear-interpolation
def calUV(point, triVertices, triUVs):

    triV = triVertices - triVertices[:, :, :, 0, np.newaxis]
    p = point - triVertices[:, :, :, 0]
    l = np.linalg.norm(triV, axis=-1) + 1e-5

    r = np.einsum('ijklm, ijkm -> ijkl', triV, p)
    r /= l * l

    uvStack = (2 - r[:, :, :, 1, np.newaxis] - r[:, :, :, 2, np.newaxis]) * triUVs[:, :, :, 0] / 2
    uvStack += r[:, :, :, 1, np.newaxis] * triUVs[:, :, :, 1] / 2
    uvStack += r[:, :, :, 2, np.newaxis] * triUVs[:, :, :, 2] / 2

    # print(triVertices[4, 1, 0])
    # print(point[4, 1, 0])
    # print(triVertices[4, 100, 0])
    # print(point[4, 100, 0])
    # print(triVertices[4, 45, 0])
    # print(point[4, 45, 0])

    # uvStack = triUVs[:, :, :, 0]
    
    return uvStack
