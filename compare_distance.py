import cv2
import numpy as np
from core.utils.loader import parse_obj, save_obj
from core.utils.cut import cutLayer, cutBounding
from core.MeshBVH import MeshBVH
from core.math.Triangle import Triangle

path_1 = '../full-scrolls/Scroll1.volpkg/20231012184423/20231012184423.obj'
path_2 = '../full-scrolls/Scroll1.volpkg/20231012184424/20231012184424.obj'

# data = parse_obj(path_2)
# cutBounding(data, boxMin, boxMax)

# save_obj('cut_2.obj', data)

data_1 = parse_obj('cut_crunk_1.obj')
data_2 = parse_obj('cut_crunk_2.obj')

# boxMin = np.array([ 2683.64, 2306.33, 2000 ])
# boxMax = np.array([ 2837.26, 2409.61, 2100 ])

point = data_1['vertices']

n, _ = point.shape  
closestPoint = np.full((n, 3), 0)
closestPointIndex = np.full((n), 0)
closestDistance = np.full((n), float('inf'))

triVertices = data_2['vertices'][data_2['faces'][:,:,0] - 1]
tri = Triangle(triVertices)

for i in range(triVertices.shape[0]):
    target = tri.closestPointToPointGPU(point, i)
    d = np.linalg.norm(point - target, axis=1)
    closestDistance = np.minimum(closestDistance, d)
    closestPoint = np.where((closestDistance == d)[:, np.newaxis], target, closestPoint)

print(closestDistance)

# w, h = 100, 100
# image = np.zeros((h, w, 3), dtype=np.uint8)
# color = (255, 255, 255)

# cv2.imshow('distance', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# cutBounding(data_1, boxMin, boxMax)
# cutBounding(data_2, boxMin, boxMax)

# save_obj('cut_crunk_1.obj', data_1)
# save_obj('cut_crunk_2.obj', data_2)

# bvh = MeshBVH(data_1)

# node = bvh._roots[0].left.left.left.left.left
# print(node._offset)
# print(node._count)
# print(node.boundingData)


