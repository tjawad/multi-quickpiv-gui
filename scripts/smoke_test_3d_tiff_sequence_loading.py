"""Smoke test for loading separate 3D TIFF volumes as a 3D time series."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import tifffile

from multi_quickpiv_gui.backend.io import load_3d_tiff_sequence


def main() -> None:
    """Create tiny 3D TIFF volumes and load them as a time series."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        vol0 = np.zeros((4, 5, 6), dtype=np.uint16)
        vol1 = np.ones((4, 5, 6), dtype=np.uint16)
        vol2 = np.full((4, 5, 6), 2, dtype=np.uint16)

        paths = [
            tmp_path / "TP0001.tif",
            tmp_path / "TP0002.tif",
            tmp_path / "TP0003.tif",
        ]

        tifffile.imwrite(paths[0], vol0)
        tifffile.imwrite(paths[1], vol1)
        tifffile.imwrite(paths[2], vol2)

        loaded = load_3d_tiff_sequence(paths)

        assert loaded.shape == (3, 4, 5, 6)
        assert loaded.spatial_ndim == 3
        assert loaded.is_3d
        assert not loaded.is_2d
        assert loaded.dataset_name == "3D TIFF sequence (3 files)"
        assert np.all(loaded.data[0] == 0)
        assert np.all(loaded.data[1] == 1)
        assert np.all(loaded.data[2] == 2)

        print("3D TIFF sequence loading smoke test passed")
        print("shape:", loaded.shape)
        print("spatial_ndim:", loaded.spatial_ndim)
        print("dataset_name:", loaded.dataset_name)


if __name__ == "__main__":
    main()
