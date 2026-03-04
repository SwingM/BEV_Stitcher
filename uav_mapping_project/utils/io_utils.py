"""Input/output helper functions for image-based workflows."""

from pathlib import Path
from typing import Iterator

import cv2
import numpy as np


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


def load_images_from_folder(folder_path: Path) -> list[tuple[np.ndarray, dict[str, int | str]]]:
    """Load images and parse tile coordinates from deterministic filenames.

    Filenames expected: ``tile_x{col}_y{row}.png``.

    Args:
        folder_path: Directory containing tile images.

    Returns:
        A list of ``(image, metadata)`` tuples.
    """
    images: list[tuple[np.ndarray, dict[str, int | str]]] = []
    for image_path in _iter_image_paths(folder_path):
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            continue
        col, row = _parse_tile_coordinates(image_path.stem)
        metadata = {
            "path": str(image_path),
            "filename": image_path.name,
            "col": col,
            "row": row,
        }
        images.append((image, metadata))

    images.sort(key=lambda item: (int(item[1]["row"]), int(item[1]["col"])))
    return images


def save_image(image: np.ndarray, output_path: Path) -> None:
    """Persist an image and ensure parent folders exist."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), image):
        raise IOError(f"Failed to write image to {output_path}")


def _iter_image_paths(folder_path: Path) -> Iterator[Path]:
    if not folder_path.exists():
        raise FileNotFoundError(f"Image folder does not exist: {folder_path}")

    for path in sorted(folder_path.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def _parse_tile_coordinates(stem: str) -> tuple[int, int]:
    try:
        x_part, y_part = stem.split("_")[1:3]
        return int(x_part[1:]), int(y_part[1:])
    except (IndexError, ValueError) as exc:
        raise ValueError(
            f"Invalid tile filename format '{stem}'. Expected tile_x{{col}}_y{{row}}"
        ) from exc
