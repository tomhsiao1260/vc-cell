import nrrd
import shutil
import argparse
import tifffile
import numpy as np
from utils.draw import drawImage
from utils.volume import calculateVolume

# extract volume in the bounding box
def getVolume(boxMin, boxMax):
    volumeStack = calculateVolume(boxMin, boxMax)

    # z, y, x -> x, y, z
    nrrdStack = np.transpose(volumeStack * 255, (2, 1, 0)).astype(np.uint8)
    nrrd.write('output/volume.nrrd', nrrdStack)
    shutil.copy('output/volume.nrrd', 'client/public')
    # z, y, x -> z, y, x
    imageStack = np.transpose(volumeStack * 65535, (0, 1, 2)).astype(np.uint16)
    tifffile.imwrite('output/volume.tif', imageStack)
    # debug
    drawImage('output/volume.tif')

    return volumeStack

# python get_volume.py --center 4276.67 3326.57 6702.28 --size 150 100 120
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate volume via boudning box')
    parser.add_argument('--center', nargs=3, type=float, metavar=('X', 'Y', 'Z'), help='bounding box center (x, y, z)')
    parser.add_argument('--size', nargs=3, type=int, metavar=('X', 'Y', 'Z'), help='bounding box size (w, h, d)')
    args = parser.parse_args()

    center = np.array(args.center)
    boxSize = np.array(args.size)
    boxMin = center - boxSize / 2
    boxMax = center + boxSize / 2
    getVolume(boxMin, boxMax)
