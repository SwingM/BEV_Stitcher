"""Shared map data structures for stitched-map outputs."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GlobalMap:
    """Container for stitched image and world-scale metadata."""

    image: np.ndarray
    resolution: float
    origin: tuple[float, float]
