"""Executable test script for grid-based stitching."""

from config import CONFIG
from stitcher.grid_stitcher import GridStitcher
from utils.io_utils import load_images_from_folder, save_image


def main() -> None:
    data_dir = CONFIG.data_dir
    tile_dir = data_dir / "tiles"
    stitched_output = data_dir / "stitched_map.png"

    tile_entries = load_images_from_folder(tile_dir)
    stitcher = GridStitcher()

    for tile_image, metadata in tile_entries:
        stitcher.add_tile(tile_image, metadata)

    stitched_map = stitcher.build_map()
    save_image(stitched_map, stitched_output)

    print(f"Loaded {len(tile_entries)} tiles from {tile_dir}")
    print(f"Stitched map saved to {stitched_output}")


if __name__ == "__main__":
    main()
