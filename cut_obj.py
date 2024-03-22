import argparse
import numpy as np
from path_utils import obj_path
from core.utils.loader import parse_obj, save_obj
from core.utils.cut import cutLayer, cutBounding

# python cut_obj.py --xmin 4226.67 --ymin 3276.57 --zmin 6652.28 --xmax 4326.67 --ymax 3376.57 --zmax 6752.28
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate volume via boudning box')
    parser.add_argument('--output', type=str, help='OBJ output path')
    parser.add_argument('--xmin', type=float, help='x value of bounding box minimum')
    parser.add_argument('--ymin', type=float, help='y value of bounding box minimum')
    parser.add_argument('--zmin', type=float, help='z value of bounding box minimum')
    parser.add_argument('--xmax', type=float, help='x value of bounding box maximum')
    parser.add_argument('--ymax', type=float, help='y value of bounding box maximum')
    parser.add_argument('--zmax', type=float, help='z value of bounding box maximum')
    args = parser.parse_args()

    boxMin = np.array([ args.xmin, args.ymin,args.zmin ])
    boxMax = np.array([ args.xmax, args.ymax,args.zmax ])

    data = parse_obj(obj_path)
    # cut a given .obj along z-axis
    cutLayer(data, layerMin = boxMin[2], layerMax = boxMax[2])
    # cut a given .obj along bounding box
    cutBounding(data, boxMin, boxMax)

    save_obj('output/segment.obj', data)