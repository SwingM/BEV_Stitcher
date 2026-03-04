"""Image splitting module for simulation-ready tile generation."""

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from uav_mapping_project.utils.io_utils import save_image


@dataclass(frozen=True)
class SplitMetadata:
    """Metadata that describes each generated tile."""

    row: int
    col: int
    x_start: int
    y_start: int
    width: int
    height: int
    filename: str


class ImageSplitter:
    """Split large map images into fixed-size tiles with optional overlap."""

    def __init__(self, tile_size: tuple[int, int], overlap: int = 0) -> None:
        self.tile_width, self.tile_height = tile_size
        self.overlap = overlap
        if self.overlap < 0:
            raise ValueError("Overlap must be non-negative")
        if self.tile_width <= self.overlap or self.tile_height <= self.overlap:
            raise ValueError("Tile dimensions must be greater than overlap")

    def split_image(self, image: np.ndarray, output_dir: Path) -> list[SplitMetadata]:
        """Split an image and save all tiles using deterministic file names."""
        output_dir.mkdir(parents=True, exist_ok=True)
        image_height, image_width = image.shape[:2]
        step_x = self.tile_width - self.overlap
        step_y = self.tile_height - self.overlap

        metadata: list[SplitMetadata] = []
        row_index = 0
        for y in range(0, image_height, step_y):
            col_index = 0
            for x in range(0, image_width, step_x):
                x_end = min(x + self.tile_width, image_width)
                y_end = min(y + self.tile_height, image_height)

                tile = image[y:y_end, x:x_end]
                filename = f"tile_x{col_index}_y{row_index}.png"
                save_image(tile, output_dir / filename)

                metadata.append(
                    SplitMetadata(
                        row=row_index,
                        col=col_index,
                        x_start=x,
                        y_start=y,
                        width=x_end - x,
                        height=y_end - y,
                        filename=filename,
                    )
                )
                col_index += 1
            row_index += 1

        return metadata

    @staticmethod
    def load_image(image_path: Path) -> np.ndarray:
        """Load a color image from disk."""
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(f"Unable to read input image: {image_path}")
        return image
