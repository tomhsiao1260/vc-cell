import nrrd
import shutil
import tifffile
import argparse
import numpy as np
from path_utils import label_path
from utils.draw import drawImage
from core.utils.loader import parse_obj
from utils.sdf import calculateSDF, calculateUV, calculateLabel

# distance field calculation
def getSDF(data, boxMin, boxMax):
    pStack, iStack, dStack = calculateSDF(data, boxMin, boxMax)
    dStack *= 255

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(dStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('output/sdf.nrrd', nrrdStack)
    shutil.copy('output/sdf.nrrd' , 'client/public')
    # z, x, y -> z, y, x
    imageStack = np.transpose(dStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('output/sdf.png', imageStack)
    # debug
    # drawImage('output/sdf.png')

    return pStack, iStack, dStack

# inklabels 3D mapping
def getLabel(data, pStack, iStack, path):
    indices = data['faces'][iStack][:, :, :, :, 0] - 1
    triUVs = data['uvs'][indices]
    triVertices = data['vertices'][indices]

    uvStack = calculateUV(pStack, triVertices, triUVs)
    labelStack = calculateLabel(path, uvStack)
    labelStack *= 255

    # z, x, y -> x, y, z
    nrrdStack = np.transpose(labelStack, (1, 2, 0)).astype(np.uint8)
    nrrd.write('output/inklabels.nrrd', nrrdStack)
    shutil.copy('output/inklabels.nrrd' , 'client/public')
    # z, x, y -> z, y, x
    imageStack = np.transpose(labelStack, (0, 2, 1)).astype(np.uint8)
    tifffile.imwrite('output/inklabels.png', imageStack)
    # debug
    # drawImage('output/inklabels.png')

    return labelStack

# python get_label.py --i output/segment.obj --center 4276.67 3326.57 6702.28 --size 150 100 120
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate volume via boudning box')
    parser.add_argument('--i', type=str, help='OBJ input path')
    parser.add_argument('--center', nargs=3, type=float, metavar=('X', 'Y', 'Z'), help='bounding box center (x, y, z)')
    parser.add_argument('--size', nargs=3, type=int, metavar=('X', 'Y', 'Z'), help='bounding box size (w, h, d)')
    args = parser.parse_args()

    center = np.array(args.center)
    boxSize = np.array(args.size)
    boxMin = center - boxSize / 2
    boxMax = center + boxSize / 2

    # extract sdf
    data = parse_obj(args.i)
    print('Distance field calculating ...')
    pStack, iStack, dStack = getSDF(data, boxMin, boxMax)

    # extract inklabels
    print('Inklabels calculating ...')
    getLabel(data, pStack, iStack, label_path)