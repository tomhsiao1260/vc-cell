import argparse
import numpy as np
from utils.volume import getGridName
from core.utils.loader import parse_obj
from path_utils import obj_path

# python find_grid.py --u 0.521 --v 0.492
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Calculate which grids are required.')
    parser.add_argument('--u', type=float, help='U value in UV coordinate')
    parser.add_argument('--v', type=float, help='V value in UV coordinate')
    args = parser.parse_args()

    data = parse_obj(obj_path)
    uv = np.array([ args.u, args.v ])
    d = np.sum((data['uvs'] - uv) ** 2, axis=1)
    index = np.argmin(d)

    center = data['vertices'][index]
    boxMin = center - np.array([50, 50, 50])
    boxMax = center + np.array([50, 50, 50])
    nameList = getGridName(boxMin, boxMax)

    print('The following grids are required:')
    for grid in nameList: print(grid)
    print('')
    print('Volume Minimum:')
    print(f'--xmin {boxMin[0]} --ymin {boxMin[1]} --zmin {boxMin[2]}')
    print('')
    print('Volume Maximum:')
    print(f'--xmax {boxMax[0]} --ymax {boxMax[1]} --zmax {boxMax[2]}')
    print('')


