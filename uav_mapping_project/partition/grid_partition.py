"""Grid-based partitioner for splitting maps into connected rectangular regions."""

import math

import numpy as np

from partition.base_partition import BasePartitioner


class GridPartitioner(BasePartitioner):
    """Partition a map into near-equal connected rectangular cells."""

    def partition(self, map_image: np.ndarray, num_regions: int) -> list[tuple[int, int, int, int]]:
        if num_regions <= 0:
            raise ValueError("num_regions must be greater than zero")

        height, width = map_image.shape[:2]

        rows = int(math.floor(math.sqrt(num_regions)))
        cols = int(math.ceil(num_regions / rows))

        x_bounds = np.linspace(0, width, cols + 1, dtype=int)
        y_bounds = np.linspace(0, height, rows + 1, dtype=int)

        regions: list[tuple[int, int, int, int]] = []
        for row in range(rows):
            for col in range(cols):
                if len(regions) >= num_regions:
                    break
                x_min = int(x_bounds[col])
                x_max = int(x_bounds[col + 1])
                y_min = int(y_bounds[row])
                y_max = int(y_bounds[row + 1])
                regions.append((x_min, y_min, x_max, y_max))

        return regions
