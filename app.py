import numpy as np
from utils.loader import parse_obj
from utils.computeBoundsUtils import computeTriangleBounds

if __name__ == "__main__":
    # obj_name = 'traingle.obj'
    obj_name = 'quad.obj'

    data = parse_obj(obj_name)
    data = computeTriangleBounds(data)