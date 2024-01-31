import cv2
import numpy as np

def parse_obj(filename):
    vertices = []
    normals = []
    uvs = []
    faces = []
    colors = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('v '):
                data = [float(x) for x in line[2:].split()]
                vertices.append(data[:3])
                colors.append(data[3:])
            elif line.startswith('vn '):
                normals.append([float(x) for x in line[3:].split()])
            elif line.startswith('vt '):
                uvs.append([float(x) for x in line[3:].split()])
            elif line.startswith('f '):
                triangle = [x.split('/') for x in line.split()[1:]]
                triangle = [[int(x) for x in vertex] for vertex in triangle]
                faces.append(triangle)

    data = {}
    data['vertices']    = np.array(vertices)
    data['normals']     = np.array(normals)
    data['uvs']         = np.array(uvs)
    data['faces']       = np.array(faces)
    data['colors']      = np.array(colors)

    return data

segmentID = '20230702185753'

layer = 1050
scrollX = 8096
scrollY = 7888
scrollZ = 14370

obj_name   = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
label_name = '20230702185753_inklabels.png'

data = parse_obj(obj_name)
label = cv2.imread(label_name, cv2.IMREAD_UNCHANGED)

mask = np.abs(data['vertices'][:, 2] - layer) < 100
p = data['vertices'][mask]
uv = data['uvs'][mask]

h, w = label.shape
image1 = np.zeros((h, w, 3), dtype=np.uint8)
image2 = np.zeros((scrollY, scrollX, 3), dtype=np.uint16)

for point in uv:
    x = int(point[0] * w)
    y = int((1 - point[1]) * h)
    image1[y, x] = (255, 255, 255)

cv2.imshow('Image', image1)
cv2.waitKey(0)
cv2.destroyAllWindows()

for point in p:
    x = int(point[0])
    y = int(point[1])
    image2[y, x] = (65535, 65535, 65535)

cv2.imshow('Image', image2)
cv2.waitKey(0)
cv2.destroyAllWindows()



