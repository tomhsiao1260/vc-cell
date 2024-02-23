import numpy as np
from utils.loader import parse_obj
from utils.computeBoundsUtils import getBounds, computeTriangleBounds

if __name__ == "__main__":
    # obj_name = 'traingle.obj'
    # obj_name = 'quad.obj'
    obj_name = 'plane.obj'

    data = parse_obj(obj_name)
    box_centers, box_half_sizes = computeTriangleBounds(data)
    getBounds(box_centers, box_half_sizes)
