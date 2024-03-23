import argparse
import numpy as np
from path_utils import obj_path
from core.utils.loader import parse_obj, save_obj
from core.utils.cut import cutLayer, cutBounding

# python cut_obj.py --o output/segment.obj --center 4276.67 3326.57 6702.28 --size 150 100 120
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate volume via boudning box')
    parser.add_argument('--o', type=str, help='OBJ output path')
    parser.add_argument('--center', nargs=3, type=float, metavar=('X', 'Y', 'Z'), help='bounding box center (x, y, z)')
    parser.add_argument('--size', nargs=3, type=int, metavar=('X', 'Y', 'Z'), help='bounding box size (w, h, d)')
    args = parser.parse_args()

    center = np.array(args.center)
    boxSize = np.array(args.size)
    boxMin = center - boxSize / 2
    boxMax = center + boxSize / 2

    data = parse_obj(obj_path)
    # cut a given .obj along z-axis
    cutLayer(data, layerMin = boxMin[2], layerMax = boxMax[2])
    # cut a given .obj along bounding box
    cutBounding(data, boxMin, boxMax)

    save_obj(args.o, data)