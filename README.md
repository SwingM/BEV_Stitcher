# UAV Mapping Project

A clean, modular Python project for UAV mapping simulation:

1. Split a large map into deterministic tiles.
2. Stitch tiles into a global bird's-eye-view (BEV) map.
3. Partition the stitched map into exploration regions with pixel and metric bounding boxes.

The code is ROS-agnostic and designed for future integration with ROS2 message adapters.

## Project Structure

```text
uav_mapping_project/
├── main.py
├── config.py
├── splitter/
│   ├── image_splitter.py
│   └── test_splitter.py
├── stitcher/
│   ├── base_stitcher.py
│   ├── global_map.py
│   ├── grid_stitcher.py
│   └── test_stitcher.py
├── partition/
│   ├── base_partition.py
│   ├── region.py
│   ├── grid_partition.py
│   └── test_partition.py
├── utils/
│   ├── io_utils.py
│   └── visualization.py
└── data/
```

## Requirements

- Python 3.10+
- `numpy`
- `opencv-python`
- `matplotlib`

Install dependencies:

```bash
python -m pip install numpy opencv-python matplotlib
```

## How to Run

Run commands from repository root (`BEV_Stitcher`).

### 1) Generate synthetic source map and split into tiles

```bash
python -m uav_mapping_project.splitter.test_splitter
```

Outputs:

- `uav_mapping_project/data/source_map.png`
- `uav_mapping_project/data/split_grid_preview.png`
- `uav_mapping_project/data/tiles/tile_x{col}_y{row}.png`

### 2) Stitch tiles into global map

```bash
python -m uav_mapping_project.stitcher.test_stitcher
```

Outputs:

- `uav_mapping_project/data/stitched_map.png`

Console also prints map resolution (meters/pixel) and origin.

### 3) Partition stitched map into regions

```bash
python -m uav_mapping_project.partition.test_partition
```

Outputs:

- `uav_mapping_project/data/partition_overlay.png`

Console prints each region in:

- pixel coordinates: `bbox_pixel`
- metric coordinates: `bbox_meter`

### 4) Run full end-to-end pipeline

```bash
python -m uav_mapping_project.main
```

This executes split → stitch → partition in sequence and writes results under `uav_mapping_project/data/`.

## Configuration

Edit `uav_mapping_project/config.py` to customize:

- tile size and overlap
- synthetic map size
- number of partition regions
- camera/UAV parameters (`altitude`, `fx`, `fy`, `cx`, `cy`, image size)
- default map origin and fallback resolution

## Notes for Integration

- `GlobalMap` includes:
  - `image`
  - `resolution` (meters per pixel)
  - `origin` (world coordinate for top-left)
- Partition output `Region` includes both `bbox_pixel` and `bbox_meter`.
- No ROS imports are used; conversion to ROS2 messages can be added in a separate adapter layer.
