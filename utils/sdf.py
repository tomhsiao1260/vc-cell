import os
import cv2
import nrrd
import shutil
import tifffile
import numpy as np
from tqdm import tqdm
from core.math.Triangle import Triangle

def calSDF(data):
    boxMin = np.min(data['vertices'], axis=0)
    boxMax = np.max(data['vertices'], axis=0)

    layerMin = int(boxMin[2]) + 50
    # layerMin = int(boxMin[2])
    layerMax = int(boxMin[2]) + 52
    # layerMax = int(boxMax[2])
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

        closestPoint, closestPointIndex, closestDistance = closestPointToPoint(data, p, layer)
        d = closestDistance / maxDistance
        indexStack.append(closestPointIndex)
        pointStack.append(closestPoint)
        dStack.append(d)

    indices = np.array(indexStack)
    point = np.array(pointStack)
    indices = data['faces'][indices][:, :, :, :, 0] - 1

    triUVs = data['uvs'][indices]
    triVertices = data['vertices'][indices]
    uvStack = calculateUV(point, triVertices, triUVs)

    # extract inklabel from 2d uv to 3d stack
    image = cv2.imread('model/SPOILER_20230702185753.png', cv2.IMREAD_UNCHANGED)
    image = image / np.max(image)
    wPixel = uvStack[:, :, :, 0]
    hPixel = 1 - uvStack[:, :, :, 1]
    hPixel = (image.shape[0] * hPixel).astype(int)
    wPixel = (image.shape[1] * wPixel).astype(int)
    inklabelStack = image[hPixel, wPixel][:,:,:]

    dStack = np.array(dStack)
    inklabelStack = np.array(inklabelStack)

    return dStack, inklabelStack

def closestPointToPoint(data, point, layer):
    w, h, _ = point.shape    
    closestPoint = np.full((w, h, 3), 0)
    closestPointIndex = np.full((w, h), 0)
    closestDistance = np.full((w, h), float('inf'))

    gap = 30
    triVertices = data['vertices'][data['faces'][:,:,0] - 1]
    lowerBound = triVertices[:,0,2] > (layer - gap)
    upperBound = triVertices[:,0,2] < (layer + gap)
    mask = np.logical_and(lowerBound, upperBound)
    index = np.nonzero(mask)[0]
    triVertices = triVertices[mask]
    tri = Triangle(triVertices)

    for i in range(triVertices.shape[0]):
        target = tri.closestPointToPointGPU(point, i)
        d = np.linalg.norm(point - target, axis=2)
        closestDistance = np.minimum(closestDistance, d)
        closestPoint = np.where((closestDistance == d)[:, :, np.newaxis], target, closestPoint)
        closestPointIndex = np.where((closestDistance == d), index[i], closestPointIndex)

    return closestPoint, closestPointIndex, closestDistance

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

    # extract inklabel from 2d uv to 3d stack
    image = cv2.imread('model/SPOILER_20230702185753.png')
    wPixel = uvStack[:, :, :, 0]
    hPixel = 1 - uvStack[:, :, :, 1]
    hPixel = (image.shape[0] * hPixel).astype(int)
    wPixel = (image.shape[1] * wPixel).astype(int)
    inklabelStack = image[hPixel, wPixel][:,:,:,0]

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
