"""Abstract interface for region partitioners."""

from abc import ABC, abstractmethod

import numpy as np


class BasePartitioner(ABC):
    """Defines a replaceable API for map region partitioning."""

    @abstractmethod
    def partition(self, map_image: np.ndarray, num_regions: int) -> list[tuple[int, int, int, int]]:
        """Split the map into connected exploration regions."""
