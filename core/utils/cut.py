import numpy as np

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
    
def cut_obj(data, splitAxis, splitOffset, survive):
    triVertices = data['vertices'][data['faces'][:,:,0] - 1]

    # number of vertices of each triangle located in the lower side (0~3)
    tri_lower_num = np.sum(triVertices[:, :, splitAxis] < splitOffset, axis=1)
    if (survive == 'left'):  data['faces'] = data['faces'][tri_lower_num >= 2]
    if (survive == 'right'): data['faces'] = data['faces'][tri_lower_num < 2]

    return data

# cut a given obj along z-axis
def cutLayer(data, layerMin, layerMax):
    # cut z
    cut_obj(data, splitAxis = 2, splitOffset = layerMin, survive = 'right')
    cut_obj(data, splitAxis = 2, splitOffset = layerMax, survive = 'left')

    re_index(data)
    return data

# cut a given obj via a bounding box
def cutBounding(data, boxMin, boxMax):
    # cut x
    cut_obj(data, splitAxis = 0, splitOffset = boxMin[0], survive = 'right')
    cut_obj(data, splitAxis = 0, splitOffset = boxMax[0], survive = 'left')
    # cut y
    cut_obj(data, splitAxis = 1, splitOffset = boxMin[1], survive = 'right')
    cut_obj(data, splitAxis = 1, splitOffset = boxMax[1], survive = 'left')
    # cut z
    cut_obj(data, splitAxis = 2, splitOffset = boxMin[2], survive = 'right')
    cut_obj(data, splitAxis = 2, splitOffset = boxMax[2], survive = 'left')

    re_index(data)
    return data