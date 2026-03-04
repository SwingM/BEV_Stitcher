"""Executable test script for map partitioning."""

import cv2

from config import CONFIG
from partition.grid_partition import GridPartitioner
from utils.io_utils import save_image
from utils.visualization import draw_partition_overlay


def main() -> None:
    stitched_map_path = CONFIG.data_dir / "stitched_map.png"
    output_path = CONFIG.data_dir / "partition_overlay.png"

    map_image = cv2.imread(str(stitched_map_path), cv2.IMREAD_COLOR)
    if map_image is None or map_image.size == 0:
        raise FileNotFoundError(
            f"Stitched map not found at {stitched_map_path}. Run test_stitcher.py first."
        )

    partitioner = GridPartitioner()
    regions = partitioner.partition(map_image, CONFIG.num_regions)

    overlay = draw_partition_overlay(map_image, regions)
    save_image(overlay, output_path)

    print(f"Partition count: {len(regions)}")
    print(f"Overlay saved to: {output_path}")


if __name__ == "__main__":
    main()
