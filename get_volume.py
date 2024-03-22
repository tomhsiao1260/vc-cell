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
    volumeStack *= 255

    # z, y, x -> x, y, z
    nrrdStack = np.transpose(volumeStack, (2, 1, 0)).astype(np.uint8)
    nrrd.write('output/volume.nrrd', nrrdStack)
    shutil.copy('output/volume.nrrd', 'client/public')
    # z, y, x -> z, y, x
    imageStack = np.transpose(volumeStack, (0, 1, 2)).astype(np.uint8)
    tifffile.imwrite('output/volume.png', imageStack)
    # debug
    # drawImage('output/volume.png')

    return volumeStack

# python get_volume.py --min 4226.67 3276.57 6652.28 --max 4326.67 3376.57 6752.28
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate volume via boudning box')
    parser.add_argument('--min', nargs=3, type=float, metavar=('X', 'Y', 'Z'), help='x, y, z value of bounding box minimum')
    parser.add_argument('--max', nargs=3, type=float, metavar=('X', 'Y', 'Z'), help='x, y, z value of bounding box maximum')
    args = parser.parse_args()

    boxMin = np.array(args.min)
    boxMax = np.array(args.max)
    getVolume(boxMin, boxMax)