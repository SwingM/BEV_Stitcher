"""Region data structures for partition outputs."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    """Connected exploration region expressed in pixel and metric spaces."""

    id: int
    bbox_pixel: tuple[int, int, int, int]
    bbox_meter: tuple[float, float, float, float]
