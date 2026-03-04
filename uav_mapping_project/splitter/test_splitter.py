"""Executable test script for the image splitter module."""

import cv2
import numpy as np

from uav_mapping_project.config import CONFIG
from uav_mapping_project.splitter.image_splitter import ImageSplitter
from uav_mapping_project.utils.io_utils import save_image
from uav_mapping_project.utils.visualization import draw_grid_overlay


def _build_synthetic_map(size: tuple[int, int]) -> np.ndarray:
    height, width = size
    image = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        image[y, :, 1] = int(255 * y / max(1, height - 1))
    for x in range(width):
        image[:, x, 2] = int(255 * x / max(1, width - 1))

    cv2.circle(image, (width // 3, height // 3), 80, (255, 255, 0), thickness=5)
    cv2.rectangle(image, (width // 2, height // 2), (width - 80, height - 120), (0, 255, 255), 4)
    cv2.putText(image, "SYNTHETIC MAP", (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
    return image


def main() -> None:
    data_dir = CONFIG.data_dir
    source_path = data_dir / "source_map.png"
    tile_dir = data_dir / "tiles"

    data_dir.mkdir(parents=True, exist_ok=True)
    source_image = _build_synthetic_map(CONFIG.synthetic_map_size)
    save_image(source_image, source_path)

    splitter = ImageSplitter(tile_size=CONFIG.tile_size, overlap=CONFIG.overlap)
    split_metadata = splitter.split_image(source_image, tile_dir)

    grid_preview = draw_grid_overlay(source_image, CONFIG.tile_size[0], CONFIG.tile_size[1])
    save_image(grid_preview, data_dir / "split_grid_preview.png")

    print(f"Input map: {source_path}")
    print(f"Tiles saved to: {tile_dir}")
    print(f"Generated tile count: {len(split_metadata)}")


if __name__ == "__main__":
    main()
