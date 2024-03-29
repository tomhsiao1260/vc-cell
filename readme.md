<h1 align="center">VC cell</h1>

<p align="center">
    <img src="https://github.com/tomhsiao1260/vc-cell/assets/31985811/2a336bc3-f7fa-42c8-b865-347fa63b2e0e" width="800px"/>
</p>

## Introduction

A Vesuvius Challenge tool to view a small volume region with high resolution and flexibility.

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

<p align="center">
<img width="226" alt="label" src="https://github.com/tomhsiao1260/vc-cell/assets/31985811/c1c4fec9-0189-4ca5-9622-170a8533d1f1">
</p>

Let's say you have a labeled image of a segment, but some local areas have some interesting behaviors that make you want to take a closer look. Take the spot above in segment `20230702185753` as an example, the uv coordinate of that spot is around `(0.521, 0.492)` (lower left and upper right corner are (0, 0) and (1, 1) respectively).

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

A `volume.tif` and a `volume.nrrd` will be generated in `output` folder. These two files are the same data in the same area. The tif version is for you to view or process further. The nrrd version is for rendering in browser later.

## Cut the segment

Let's extract the corresponding segment obj data within this bounding box.

```bash
python cut_obj.py --o output/segment.obj --center 4276.67 3326.57 6702.28 --size 150 100 120
```

It will generate a cropped OBJ file in output folder called `segment.obj` which only preserves the data within that bounding box.

## Get the Distance Field

With the info above, in that region, we can generate inklabels in 3D space. But before that, we need to calculate the distance field. This command will generate a `sdf.tif` and `label.tif` with its corresponding `.nrrd` files.

```bash
python get_sdf.py --i output/segment.obj --center 4276.67 3326.57 6702.28 --size 150 100 120
```

`sdf.png` store the distance field info inside that bounding box. Each pixel store a normalized distance value between that point and `segment.obj`.

`label.png` store the inklabels info inside that bounding box. Each pixel stores the inklabels intensity from the nearest point on `segment.obj`.

## Get the inklabels in 3D space

With `sdf.png` and `label.png`, you can generate your own customized inklabels in 3D space. Here's a small example of how it works.

```bash
python get_label.py --sdf output/sdf.tif --label output/label.tif --o output/inklabels.tif
```

This command will generate an `inklabels.tif` in output folder which is the inklabel mapping in 3D space. You can tweak the weights in `get_label.py` to fit your use case (e.g. use `volume.tif` and `inklabels.tif` to train a neural net in this region).

If you want to go further, you can also combine `sdf.tif` generated from different segments via picking the minimum value for a given pixel position. And use those info to generate a new `inklabels.tif` for these segments. Or try to merge `sdf.tif` and `inklabels.tif` from different region to form a larger map. I think it's pretty flexible to explore!

## Visualize it on the browser

Now we can visualize all of it on your localhost browser. Please make sure [Node.js](https://nodejs.org/en/download) is downloaded and then run the following command. It will install the related packages for this application.

```bash
cd client
npm install
```

Once finished, you can start the dev server and navigate to http://localhost:5173

```bash
npm run dev
```

cheer 🌱

## Segmentation inspection / evaluation

Visually compare two flattened meshes of the same region: using a color map, for each pixel, plot the distance from segmentation(s) A to the nearest point in segmentation(s) B.

Take segment `20231012184424` as an example of A and `20231012184423` as B. To generate a map related to A to see how much difference there is from B, we need to cut them into multiple chunks in advance. It will generate a folder in `output` folder with the corresponding segment chunks (~2min).

```bash
# cut A along z-axis
python inspect_segment.py --mode preprocess --name 4424 --path 20231012184424.obj
# cut B along z-axis
python inspect_segment.py --mode preprocess --name 4423 --path 20231012184423.obj
```

Now, we can calculate the nearest distance between segments A, B. It will generate a `.npz` file which stores all the related info (~8min).

```bash
python inspect_segment.py --mode inspect --A 4424 --B 4423 --o output/inspect.npz
```

`inspect.npz` stores the nearest distance `d` and its corresponding uv coordinate `uv` for each vertices in segment A. Note that `d` can be a negative value, which means the point in segment A is below the surface of B (compared to surface normal of B), vice versa.

```python
data = np.load('output/inspect.npz')

d = data['d']
uv = data['uv']
```

There are many ways to visualize the `.npz` data. It's up to you. Here's a simple plot function as a demo.

```bash
python inspect_segment.py --mode plot --w 2336 --h 1575 --i output/inspect.npz --o output/inspect.png
```

<p align="center">
<img width="500" alt="d" src="https://github.com/tomhsiao1260/vc-cell/assets/31985811/7f6899c9-cb03-4d5b-a8f0-f1f5632ab105">
</p>

## Notes

It is also recommended to adjust the browser to a smaller border size for a smoother experience. Full screen may be a bit laggy. In addition, please don't hesitate to message me on Discord or here if you have any difficulty or questions when using it.
