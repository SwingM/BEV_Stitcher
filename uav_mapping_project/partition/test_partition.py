"""Executable test script for map partitioning."""

import cv2

from uav_mapping_project.config import CAMERA_CONFIG, CONFIG
from uav_mapping_project.partition.grid_partition import GridPartitioner
from uav_mapping_project.stitcher.global_map import GlobalMap
from uav_mapping_project.utils.io_utils import save_image
from uav_mapping_project.utils.visualization import draw_partition_overlay


def main() -> None:
    stitched_map_path = CONFIG.data_dir / "stitched_map.png"
    output_path = CONFIG.data_dir / "partition_overlay.png"

    map_image = cv2.imread(str(stitched_map_path), cv2.IMREAD_COLOR)
    if map_image is None or map_image.size == 0:
        raise FileNotFoundError(
            f"Stitched map not found at {stitched_map_path}. Run test_stitcher.py first."
        )

    resolution = CAMERA_CONFIG.altitude / CAMERA_CONFIG.fx
    global_map = GlobalMap(image=map_image, resolution=resolution, origin=CONFIG.default_origin)

    partitioner = GridPartitioner()
    regions = partitioner.partition(global_map, CONFIG.num_regions)

    overlay = draw_partition_overlay(global_map.image, regions)
    save_image(overlay, output_path)

    print(f"Partition count: {len(regions)}")
    print(f"Overlay saved to: {output_path}")
    for region in regions:
        print(
            f"Region {region.id}: px={region.bbox_pixel}, m=({region.bbox_meter[0]:.2f}, "
            f"{region.bbox_meter[1]:.2f}, {region.bbox_meter[2]:.2f}, {region.bbox_meter[3]:.2f})"
        )


if __name__ == "__main__":
    main()
