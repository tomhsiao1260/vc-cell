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

def save_obj(filename, data):
    vertices = data.get('vertices', np.array([]))
    normals  = data.get('normals' , np.array([]))
    uvs      = data.get('uvs'     , np.array([]))
    faces    = data.get('faces'   , np.array([]))
    colors   = data.get('colors'  , np.array([]))

    with open(filename, 'w') as f:

        f.write(f"# Vertices: {len(vertices)}\n")
        f.write(f"# Faces: {len(faces)}\n")

        for i in range(len(vertices)):
            vertex = vertices[i]
            normal = normals[i]
            color = colors[i] if len(colors) else ''

            f.write('v ')
            f.write(f"{' '.join(str(round(x, 2)) for x in vertex)}")
            f.write(' ')
            f.write(f"{' '.join(str(round(x, 6)) for x in color)}")
            f.write('\n')

            f.write('vn ')
            f.write(f"{' '.join(str(round(x, 6)) for x in normal)}")
            f.write('\n')

        for uv in uvs:
            f.write(f"vt {' '.join(str(round(x, 6)) for x in uv)}\n")

        for face in faces:
            indices = ' '.join(['/'.join(map(str, vertex)) for vertex in face])
            f.write(f"f {indices}\n")

def re_index(data):
    data['faces'] -= 1
    selected_vertices = np.unique(data['faces'][:,:,0])

    # only leave the vertices used to form the faces
    data['vertices'] = data['vertices'][selected_vertices]
    data['normals']  = data['normals'][selected_vertices]
    data['uvs']      = data['uvs'][selected_vertices]
    data['colors']   = data['colors'][selected_vertices]

    # update face index
    vertex_mapping = { old_index: new_index for new_index, old_index in enumerate(selected_vertices) }
    data['faces'] = np.vectorize(lambda x: vertex_mapping.get(x, x))(data['faces'])
    data['faces'] += 1

def cut_obj(data, layer, gap):
    tri_z_values = data['vertices'][data['faces'][:,:,0] - 1, 2]

    cutting_line = layer + gap
    # number of vertices of each triangle located in the lower z side (0~3)
    tri_lower_num = np.sum(data['vertices'][data['faces'][:,:,0] - 1, 2] < cutting_line, axis=1)
    data['faces'] = data['faces'][tri_lower_num >= 2]

    cutting_line = layer - gap
    # number of vertices of each triangle located in the higher z side (0~3)
    tri_higher_num = np.sum(data['vertices'][data['faces'][:,:,0] - 1, 2] > cutting_line, axis=1)
    data['faces'] = data['faces'][tri_higher_num >= 2]

    re_index(data)
    save_obj('20230702185753.obj', data)

segmentID = '20230702185753'

layer = 1050
scrollX = 8096
scrollY = 7888
scrollZ = 14370

obj_name   = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
label_name = '20230702185753_inklabels.png'

data = parse_obj(obj_name)

cut_obj(data, layer, 100)
# label = cv2.imread(label_name, cv2.IMREAD_UNCHANGED)

# mask = np.abs(data['vertices'][:, 2] - layer) < 100
# p = data['vertices'][mask]
# uv = data['uvs'][mask]

# h, w = label.shape
# image1 = np.zeros((h, w, 3), dtype=np.uint8)
# image2 = np.zeros((scrollY, scrollX, 3), dtype=np.uint16)

# for point in uv:
#     x = int(point[0] * w)
#     y = int((1 - point[1]) * h)
#     image1[y, x] = (255, 255, 255)

# cv2.imshow('Image', image1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# for point in p:
#     x = int(point[0])
#     y = int(point[1])
#     image2[y, x] = (65535, 65535, 65535)

# cv2.imshow('Image', image2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



