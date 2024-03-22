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

Volume Minimum:
--xmin 4226.67 --ymin 3276.57 --zmin 6652.28

Volume Maximum:
--xmax 4326.67 --ymax 3376.57 --zmax 6752.28
```

This means we need to download `cell_yxz_007_009_014.tif` and put it into the corresponding `grid_folder`. And the remaining info is the min and max values ​​of a volume bounding box formed around this uv coordinate.

## Get the volume

Now we can extract a small volume from `grid_folder` via previous bounding box info.

```bash
python get_volume.py --xmin 4226.67 --ymin 3276.57 --zmin 6652.28 --xmax 4326.67 --ymax 3376.57 --zmax 6752.28
```

You will receive a `volume.png` and a `volume.nrrd` in `output` folder.
