"""End-to-end UAV mapping pipeline entrypoint."""

import cv2

from uav_mapping_project.config import CAMERA_CONFIG, CONFIG
from uav_mapping_project.partition.grid_partition import GridPartitioner
from uav_mapping_project.splitter.image_splitter import ImageSplitter
from uav_mapping_project.stitcher.grid_stitcher import GridStitcher
from uav_mapping_project.utils.io_utils import load_images_from_folder, save_image
from uav_mapping_project.utils.visualization import draw_partition_overlay


def run_pipeline() -> None:
    data_dir = CONFIG.data_dir
    data_dir.mkdir(parents=True, exist_ok=True)

    source_path = data_dir / "source_map.png"
    if not source_path.exists():
        raise FileNotFoundError(
            f"{source_path} not found. Run splitter/test_splitter.py to generate synthetic map."
        )

    source_image = ImageSplitter.load_image(source_path)

    tile_dir = data_dir / "tiles"
    splitter = ImageSplitter(tile_size=CONFIG.tile_size, overlap=CONFIG.overlap)
    splitter.split_image(source_image, tile_dir)

    stitcher = GridStitcher(
        camera_config=CAMERA_CONFIG,
        default_resolution=CONFIG.default_resolution_m_per_px,
        origin=CONFIG.default_origin,
    )
    for tile_image, metadata in load_images_from_folder(tile_dir):
        stitcher.add_tile(tile_image, metadata)

    global_map = stitcher.build_map()
    save_image(global_map.image, data_dir / "stitched_map.png")

    partitioner = GridPartitioner()
    regions = partitioner.partition(global_map, CONFIG.num_regions)
    partition_overlay = draw_partition_overlay(global_map.image, regions)
    save_image(partition_overlay, data_dir / "partition_overlay.png")

    cv2.imwrite(str(data_dir / "partition_overlay_rgb.png"), cv2.cvtColor(partition_overlay, cv2.COLOR_BGR2RGB))
    print("Pipeline complete. Outputs written to data directory.")
    print(f"Map resolution (m/px): {global_map.resolution:.6f}")
    print(f"Map origin (m): {global_map.origin}")


if __name__ == "__main__":
    run_pipeline()
