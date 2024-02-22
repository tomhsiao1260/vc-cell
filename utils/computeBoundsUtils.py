from utils.constants import FLOAT32_EPSILON
import numpy as np

# computes the union of the bounds of all of the given triangles and puts the resulting box in "target".
# A bounding box is computed for the centroids of the triangles, as well, and placed in "centroidTarget".
# These are computed together to avoid redundant accesses to bounds array.
def computeTriangleBounds(data):
    vertices = data.get('vertices', np.array([]))
    faces    = data.get('faces'   , np.array([]))[:, :, 0]

    p = vertices[faces - 1]
    box_min = np.min(p, axis=1)
    box_max = np.max(p, axis=1)