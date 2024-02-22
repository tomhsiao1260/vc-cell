import cv2

if __name__ == "__main__":
    segmentID = '20230702185753'

    layer = 1050
    scrollX = 8096
    scrollY = 7888
    scrollZ = 14370

    obj_name   = f'../full-scrolls/Scroll1.volpkg/paths/{segmentID}/{segmentID}.obj'
    label_name = '20230702185753_inklabels.png'

# data = parse_obj(obj_name)

# data = cut_obj(data, layer, 100)
# re_index(data)
# save_obj(f'{segmentID}.obj', data, segmentID)

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