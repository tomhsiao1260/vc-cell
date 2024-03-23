## Introduction

A Vesuvius Challenge tool to view a small 3D region of high resolution volume with flexibility.

## Setup

Install dependency

```
pip install -r requirements.txt
```

Config `path_utils.py`.

```bash
# OBJ file of a segment
obj_path = '../full-scrolls/Scroll1.volpkg/paths/20230702185753/20230702185753.obj'

# volume gird folder
grid_folder = '../full-scrolls/Scroll1.volpkg/volume_grids/20230205180739'

# inklabel of that segment
label_path = '20230702185753_inklabels.png'
```

## Select a location

Let's say you have a labeled image of a segment, but some local areas have some interesting behaviors that make you want to take a closer look. Take the following spot in segment `20230702185753` as an example, the uv coordinate of that spot is around `(0.521, 0.492)` (lower left and upper right corner are (0, 0) and (1, 1) respectively).

<!-- need an image here -->

And run this command:

```bash
python find_grid.py --u 0.521 --v 0.492
```

The output would be something like this:

```bash
The following grids are required:
cell_yxz_007_009_014.tif

Volume Center (x, y, z):
4276.67 3326.57 6702.28

Volume Size (w, h, d):
150 100 120
```

This means we need to download `cell_yxz_007_009_014.tif` and put it into the corresponding `grid_folder`. And the remaining info is the center and size ​​of a volume bounding box formed around this uv coordinate. The center is the position of that uv coordinate in 3D space.

## Get the volume

Now we can extract a small volume from `grid_folder` via previous bounding box info.

```bash
python get_volume.py --center 4276.67 3326.57 6702.28 --size 150 100 120
```

You will generate a `volume.tif` and a `volume.nrrd` in `output` folder. These two files are the same data in the same area. The tif version is for you view or process further. The nrrd version is for rendering in browser later.

## Cut the segment

Let's extract the corresponding segment obj data within this bounding box.

```bash
python cut_obj.py --o output/segment.obj --center 4276.67 3326.57 6702.28 --size 150 100 120
```

It will generate a cropped OBJ file in output folder called `segment.obj` which only preserves the data within that bounding box.

## Get the inklabels in 3D space

With the info above, in that region, we can generate inklabels in 3D space. This command will generate a `sdf.tif` and `label.tif` in output folder with its corresponding `.nrrd` files.

```bash
python get_sdf.py --i output/segment.obj --center 4276.67 3326.57 6702.28 --size 150 100 120
```

`sdf.png` store the distance field info inside that bounding box. Each pixel store a normalized distance value between this point and `segment.obj`.

`label.png` store the inklabels info inside that bounding box. Each pixel stores the inklabels intensity from the nearest point on `segment.obj`.

With `sdf.png` and `label.png`, you can generate your own customized inklabels in 3D space. Here's just a small example of how it works.

```bash
python get_label.py
```

<!-- say what else it can be used in others use case (train nn, combine label, combine png) -->
<!-- improve js part & update readme -->
<!-- film a demo & release! -->
