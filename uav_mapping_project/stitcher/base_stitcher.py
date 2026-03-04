"""Abstract interface for map stitchers."""

from abc import ABC, abstractmethod

import numpy as np


class BaseStitcher(ABC):
    """Defines a replaceable stitching API."""

    @abstractmethod
    def add_tile(self, image: np.ndarray, metadata: dict[str, int | str]) -> None:
        """Add one tile and its metadata to the internal state."""

    @abstractmethod
    def build_map(self) -> np.ndarray:
        """Build and return the global map from all previously added tiles."""

    @abstractmethod
    def get_map(self) -> np.ndarray | None:
        """Return the already-built map, or ``None`` if not built yet."""
