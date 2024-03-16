import os
from core.MeshBVH import MeshBVH
from core.utils.cut import cut_obj, re_index
from core.utils.loader import parse_obj, save_obj
from utils.sdf import calculateSDF
from utils.draw import drawImage, drawUV, drawBoxes
from utils.volume import calculateVolume

import cv2

def cut(segmentID, layer, gap):
    path = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    data = parse_obj(path)

    data = cut_obj(data, layer, gap)
    re_index(data)
    save_obj(os.path.join('model', f'{segmentID}.obj'), data, materialName = segmentID)

if __name__ == "__main__":
    pass
    # cut(segmentID = '20230702185753', layer = 1000, gap = 50)

    # path = os.path.join('model', 'plane.obj')
    path = os.path.join('model', '20230702185753.obj')

    data = parse_obj(path)
    bvh = MeshBVH(data)

    node = bvh._roots[0].left.left.left.left
    calculateSDF(bvh, node)
    # calculateVolume(node.boundingData)

    # drawUV(bvh)
    # drawImage('model/volume.png')
    # drawLabels(bvh, indices, node)
    # drawBoxes(bvh)

    # image = cv2.imread('model/SPOILER_20230702185753.png')
    # h, w = image.shape[:2]

    # x1, x2, y1, y2 = int(w * 0.878665), int(w * 0.888363), int(h * (1 - 0.523732)), int(h * (1 - 0.505952))
    # cropped_image = image[y1:y2, x1:x2]

    # cv2.imshow('Cropped Image', cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imwrite('inklabels.png', cropped_image)



