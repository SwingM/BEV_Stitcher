"""Deterministic grid stitcher using tile coordinate metadata."""

from dataclasses import dataclass

import numpy as np

from stitcher.base_stitcher import BaseStitcher


@dataclass(frozen=True)
class TileRecord:
    """Represents one tile and grid coordinates used for reconstruction."""

    image: np.ndarray
    row: int
    col: int


class GridStitcher(BaseStitcher):
    """Stitches tiles into a global BEV map assuming perfect grid alignment."""

    def __init__(self) -> None:
        self._tiles: list[TileRecord] = []
        self._stitched_map: np.ndarray | None = None

    def add_tile(self, image: np.ndarray, metadata: dict[str, int | str]) -> None:
        row = int(metadata["row"])
        col = int(metadata["col"])
        self._tiles.append(TileRecord(image=image, row=row, col=col))

    def build_map(self) -> np.ndarray:
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

        self._stitched_map = canvas
        return canvas

    def get_map(self) -> np.ndarray | None:
        return self._stitched_map
