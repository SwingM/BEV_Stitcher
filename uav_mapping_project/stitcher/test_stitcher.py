"""Executable test script for grid-based stitching."""

from uav_mapping_project.config import CAMERA_CONFIG, CONFIG
from uav_mapping_project.stitcher.grid_stitcher import GridStitcher
from uav_mapping_project.utils.io_utils import load_images_from_folder, save_image


def main() -> None:
    data_dir = CONFIG.data_dir
    tile_dir = data_dir / "tiles"
    stitched_output = data_dir / "stitched_map.png"

    tile_entries = load_images_from_folder(tile_dir)
    stitcher = GridStitcher(
        camera_config=CAMERA_CONFIG,
        default_resolution=CONFIG.default_resolution_m_per_px,
        origin=CONFIG.default_origin,
    )

    for tile_image, metadata in tile_entries:
        stitcher.add_tile(tile_image, metadata)

    global_map = stitcher.build_map()
    save_image(global_map.image, stitched_output)

    print(f"Loaded {len(tile_entries)} tiles from {tile_dir}")
    print(f"Stitched map saved to {stitched_output}")
    print(f"Map resolution (m/px): {global_map.resolution:.6f}")
    print(f"Map origin (m): {global_map.origin}")


if __name__ == "__main__":
    main()
