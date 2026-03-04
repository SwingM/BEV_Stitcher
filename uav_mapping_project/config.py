"""Central configuration for the UAV mapping pipeline."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CameraConfig:
    """Camera and UAV parameters used for scale approximation."""

    altitude: float
    fx: float
    fy: float
    cx: float
    cy: float
    image_width: int
    image_height: int


@dataclass(frozen=True)
class PipelineConfig:
    """Configuration values shared across module tests and the main pipeline."""

    project_root: Path = Path(__file__).resolve().parent
    data_dir: Path = project_root / "data"

    # Splitter defaults
    tile_size: tuple[int, int] = (256, 256)
    overlap: int = 32

    # Partition defaults
    num_regions: int = 6

    # Synthetic map generation defaults
    synthetic_map_size: tuple[int, int] = (1024, 1024)

    # Map defaults
    default_resolution_m_per_px: float = 0.05
    default_origin: tuple[float, float] = (0.0, 0.0)


CAMERA_CONFIG = CameraConfig(
    altitude=40.0,
    fx=650.0,
    fy=650.0,
    cx=512.0,
    cy=512.0,
    image_width=1024,
    image_height=1024,
)

CONFIG = PipelineConfig()
