"""Central configuration for the UAV mapping pipeline."""

from dataclasses import dataclass
from pathlib import Path


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


CONFIG = PipelineConfig()
