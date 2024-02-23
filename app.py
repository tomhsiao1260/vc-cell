import os
import cv2
import numpy as np
from core.utils.loader import parse_obj
from core.build.buildTree import buildPackedTree

def drawBox(boundingData):
    height, width = 500, 500
    background = np.zeros((height, width, 3), dtype=np.uint8)

    xmin, ymin, zmin, xmax, ymax, zmax = boundingData[:6]

    w = abs(xmax - xmin)
    h = abs(ymax - ymin)

    box_width = int(0.75 * width)
    box_height = int(h / w * box_width)
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2

    cv2.rectangle(background, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 255, 0), thickness=2)

    cv2.imshow('Box', background)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    path = os.path.join('model', 'plane.obj')

    data = parse_obj(path)

    root = buildPackedTree(data)

    drawBox(root.boundingData)

