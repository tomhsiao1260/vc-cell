import cv2
import numpy as np 

class MeshBVHHelper:
    def __init__(self, bvh):
        self.bvh = bvh
        self.height, self.width = 500, 500
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def draw(self):
        height, width, canvas, root = self.height, self.width, self.canvas, self.bvh._roots[0]

        # self.drawBox(root.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
        
        self.drawBox(root.right.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
        self.drawBox(root.left.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
        
        # self.drawBox(root.right.right.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
        # self.drawBox(root.right.left.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
        # self.drawBox(root.left.right.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
        # self.drawBox(root.left.left.boundingData, canvas, width, height, cx = 0, cy = 0, size = 2.67)
    
        cv2.imshow('Box', canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def drawBox(self, boundingData, canvas, width, height, cx, cy, size):
        xmin, ymin, zmin, xmax, ymax, zmax = boundingData[:6]

        w = abs(xmax - xmin)
        h = abs(ymax - ymin)

        box_width = int(w / size * width)
        box_height = int(h / size * height)
        box_x = int((xmin - (cx - size / 2)) / size * width)
        box_y = int((ymin - (cy - size / 2)) / size * height)

        cv2.rectangle(canvas, (box_x, box_y), (box_x + box_width, box_y + box_height), (0, 255, 0), thickness=2)
