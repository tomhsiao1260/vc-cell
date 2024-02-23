from utils.constants import FLOAT32_EPSILON
import numpy as np

# computes the union of the bounds of all of the given triangles
def getBounds(box_centers, box_half_sizes):
    box_min = box_centers - box_half_sizes / 2
    box_max = box_centers + box_half_sizes / 2

    target_min = np.min(box_min, axis=0)
    target_max = np.max(box_max, axis=0)
    centroidTarget_min = np.min(box_centers, axis=0)
    centroidTarget_max = np.max(box_centers, axis=0)

    return target_min, target_max, centroidTarget_min, centroidTarget_max

# precomputes the bounding box for each triangle; required for quickly calculating tree splits
def computeTriangleBounds(data):
    vertices = data.get('vertices', np.array([]))
    faces    = data.get('faces'   , np.array([]))[:, :, 0]

    p = vertices[faces - 1]
    box_min = np.min(p, axis=1)
    box_max = np.max(p, axis=1)

    box_centers = (box_min + box_max) / 2
    box_half_sizes = (box_max - box_min) / 2 * (1 + FLOAT32_EPSILON)

    return box_centers, box_half_sizes
