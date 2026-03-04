"""Visualization utilities for stitched maps and region overlays."""

from typing import Sequence

import cv2
import numpy as np

from uav_mapping_project.partition.region import Region


def draw_grid_overlay(
    image: np.ndarray,
    tile_width: int,
    tile_height: int,
    color: tuple[int, int, int] = (0, 255, 0),
    thickness: int = 1,
) -> np.ndarray:
    """Draw tile-aligned grid lines on top of an image."""
    overlay = image.copy()
    height, width = overlay.shape[:2]

    for x in range(0, width, tile_width):
        cv2.line(overlay, (x, 0), (x, height), color, thickness)

    for y in range(0, height, tile_height):
        cv2.line(overlay, (0, y), (width, y), color, thickness)

    return overlay


def draw_partition_overlay(
    image: np.ndarray,
    regions: Sequence[Region],
    alpha: float = 0.35,
) -> np.ndarray:
    """Render colored bounding boxes for each region and blend with the map image."""
    base = image.copy()
    overlay = image.copy()

    palette = [
        (255, 80, 80),
        (80, 255, 80),
        (80, 80, 255),
        (255, 255, 80),
        (255, 80, 255),
        (80, 255, 255),
    ]

    for idx, region in enumerate(regions):
        x_min, y_min, x_max, y_max = region.bbox_pixel
        color = palette[idx % len(palette)]
        cv2.rectangle(overlay, (x_min, y_min), (x_max, y_max), color, thickness=-1)
        cv2.rectangle(base, (x_min, y_min), (x_max, y_max), color, thickness=2)
        cv2.putText(
            base,
            f"R{region.id}",
            (x_min + 8, y_min + 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
            lineType=cv2.LINE_AA,
        )

    blended = cv2.addWeighted(overlay, alpha, base, 1 - alpha, 0)
    return blended
