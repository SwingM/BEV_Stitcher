"""Deterministic grid stitcher using tile coordinate metadata."""

from dataclasses import dataclass

import numpy as np

from uav_mapping_project.config import CameraConfig
from uav_mapping_project.stitcher.base_stitcher import BaseStitcher
from uav_mapping_project.stitcher.global_map import GlobalMap


@dataclass(frozen=True)
class TileRecord:
    """Represents one tile and grid coordinates used for reconstruction."""

    image: np.ndarray
    row: int
    col: int


class GridStitcher(BaseStitcher):
    """Stitches tiles into a global BEV map assuming perfect grid alignment."""

    def __init__(
        self,
        camera_config: CameraConfig | None = None,
        default_resolution: float = 0.05,
        origin: tuple[float, float] = (0.0, 0.0),
    ) -> None:
        self._tiles: list[TileRecord] = []
        self._global_map: GlobalMap | None = None
        self._camera_config = camera_config
        self._default_resolution = default_resolution
        self._origin = origin

    def add_tile(self, image: np.ndarray, metadata: dict[str, int | str]) -> None:
        row = int(metadata["row"])
        col = int(metadata["col"])
        self._tiles.append(TileRecord(image=image, row=row, col=col))

    def build_map(self) -> GlobalMap:
        if not self._tiles:
            raise ValueError("No tiles have been added to stitch")

        max_row = max(tile.row for tile in self._tiles)
        max_col = max(tile.col for tile in self._tiles)

        tile_height = max(tile.image.shape[0] for tile in self._tiles)
        tile_width = max(tile.image.shape[1] for tile in self._tiles)
        channels = self._tiles[0].image.shape[2]

        canvas_height = (max_row + 1) * tile_height
        canvas_width = (max_col + 1) * tile_width
        canvas = np.zeros((canvas_height, canvas_width, channels), dtype=self._tiles[0].image.dtype)

        for tile in self._tiles:
            y_start = tile.row * tile_height
            x_start = tile.col * tile_width
            y_end = y_start + tile.image.shape[0]
            x_end = x_start + tile.image.shape[1]
            canvas[y_start:y_end, x_start:x_end] = tile.image

        resolution = self._compute_meters_per_pixel()
        self._global_map = GlobalMap(image=canvas, resolution=resolution, origin=self._origin)
        return self._global_map

    def get_map(self) -> GlobalMap | None:
        return self._global_map

    def _compute_meters_per_pixel(self) -> float:
        if self._camera_config is None:
            return self._default_resolution
        if self._camera_config.fx <= 0:
            raise ValueError("Camera fx must be positive to compute meters-per-pixel")
        return self._camera_config.altitude / self._camera_config.fx
