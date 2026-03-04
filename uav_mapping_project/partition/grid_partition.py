"""Grid-based partitioner for splitting maps into connected rectangular regions."""

import math

import numpy as np

from uav_mapping_project.partition.base_partition import BasePartitioner
from uav_mapping_project.partition.region import Region
from uav_mapping_project.stitcher.global_map import GlobalMap


class GridPartitioner(BasePartitioner):
    """Partition a map into near-equal connected rectangular cells."""

    def partition(self, global_map: GlobalMap, num_regions: int) -> list[Region]:
        if num_regions <= 0:
            raise ValueError("num_regions must be greater than zero")

        height, width = global_map.image.shape[:2]

        rows = int(math.floor(math.sqrt(num_regions)))
        cols = int(math.ceil(num_regions / rows))

        x_bounds = np.linspace(0, width, cols + 1, dtype=int)
        y_bounds = np.linspace(0, height, rows + 1, dtype=int)

        regions: list[Region] = []
        region_id = 0
        for row in range(rows):
            for col in range(cols):
                if len(regions) >= num_regions:
                    break

                x_min = int(x_bounds[col])
                x_max = int(x_bounds[col + 1])
                y_min = int(y_bounds[row])
                y_max = int(y_bounds[row + 1])

                bbox_pixel = (x_min, y_min, x_max, y_max)
                bbox_meter = self._pixel_to_meter_bbox(bbox_pixel, global_map)
                regions.append(Region(id=region_id, bbox_pixel=bbox_pixel, bbox_meter=bbox_meter))
                region_id += 1

        return regions

    @staticmethod
    def _pixel_to_meter_bbox(
        bbox_pixel: tuple[int, int, int, int], global_map: GlobalMap
    ) -> tuple[float, float, float, float]:
        x_min, y_min, x_max, y_max = bbox_pixel
        ox, oy = global_map.origin
        res = global_map.resolution
        return (
            ox + x_min * res,
            oy + y_min * res,
            ox + x_max * res,
            oy + y_max * res,
        )
