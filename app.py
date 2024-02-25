import os
import cv2
import numpy as np
from core.math.Triangle import Triangle
from core.utils.loader import parse_obj
from core.build.buildTree import buildPackedTree

def drawBox(boundingData, canvas, width, height, cx, cy, size):
    xmin, ymin, zmin, xmax, ymax, zmax = boundingData[:6]

    w = abs(xmax - xmin)
    h = abs(ymax - ymin)

    box_width = int(w / size * width)
    box_height = int(h / size * height)
    box_x = int((xmin - (cx - size / 2)) / size * width)
    box_y = int((ymin - (cy - size / 2)) / size * height)

    print(box_x, box_y, box_width, box_height)

    cv2.rectangle(canvas, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 255, 0), thickness=2)


if __name__ == "__main__":
    path = os.path.join('model', 'plane.obj')

    data = parse_obj(path)

    tri = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    T = Triangle(tri)

    p1 = np.array([-1, -1, 3])
    p2 = np.array([-1, 0.5, -3])
    p3 = np.array([0, 2, 3])
    p4 = np.array([1, 1, -3])
    p5 = np.array([2, 0, 3])
    p6 = np.array([0.5, -2, -3])
    p7 = np.array([0.5, 0.5, 3])

    print(T.closestPointToPoint(p1))
    print(T.closestPointToPoint(p2))
    print(T.closestPointToPoint(p3))
    print(T.closestPointToPoint(p4))
    print(T.closestPointToPoint(p5))
    print(T.closestPointToPoint(p6))
    print(T.closestPointToPoint(p7))

    # root = buildPackedTree(data)

    # height, width = 500, 500
    # canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # drawBox(root.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)

    # drawBox(root.right.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
    # drawBox(root.left.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)

    # drawBox(root.right.right.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
    # drawBox(root.right.left.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
    # drawBox(root.left.right.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
    # drawBox(root.left.left.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)

    # cv2.imshow('Box', canvas)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

