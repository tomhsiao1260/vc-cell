import os
import numpy as np
from core.utils.loader import parse_obj
from core.build.buildTree import buildPackedTree

if __name__ == "__main__":
    path = os.path.join('model', 'plane.obj')

    data = parse_obj(path)

    buildPackedTree(data)
