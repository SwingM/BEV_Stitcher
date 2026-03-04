"""Abstract interface for region partitioners."""

from abc import ABC, abstractmethod

from uav_mapping_project.partition.region import Region
from uav_mapping_project.stitcher.global_map import GlobalMap


class BasePartitioner(ABC):
    """Defines a replaceable API for map region partitioning."""

    @abstractmethod
    def partition(self, global_map: GlobalMap, num_regions: int) -> list[Region]:
        """Split the map into connected exploration regions."""
