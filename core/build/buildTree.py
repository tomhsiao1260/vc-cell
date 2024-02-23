import numpy as np
from core.MeshBVHNode import MeshBVHNode
from core.build.splitUtils import getOptimalSplit
from core.build.computeBoundsUtils import getBounds, computeTriangleBounds

def buildTree(triangleBounds, offset, count):
    centroidTarget = np.zeros(6, dtype=np.float32)

    root = MeshBVHNode()
    getBounds(triangleBounds, offset, count, root.boundingData, centroidTarget)
    splitNode(root, offset, count, centroidTarget)

    return root

# either recursively splits the given node, creating left and right subtrees for it, or makes it a leaf node,
# recording the offset and count of its triangles and writing them into the reordered geometry index.
def splitNode(node, offset, count, centroidBoundingData, depth = 0):
    maxLeafTris = 5

    # early out if we've met our capacity
    if (count <= maxLeafTris):
        setattr(node, "offset", offset)
        setattr(node, "count", count)
        return node
    
    axis, pos = getOptimalSplit(centroidBoundingData)

    setattr(node, "splitAxis", axis)

def buildPackedTree(data):
    triangleBounds = computeTriangleBounds(data)

    offset = 0
    count = triangleBounds[0].shape[0]

    root = buildTree(triangleBounds, offset, count)
