"""Smoke test for 3D median-despike post-processing."""

from __future__ import annotations

import numpy as np

from multi_quickpiv_gui.backend.core import apply_postprocessing
from multi_quickpiv_gui.workflow.params import (
    MedianDespikeParams,
    PIVRunParams,
    PostProcessParams,
    WorkflowParams,
)


def main() -> None:
    """Run a tiny 3D median-despike smoke test."""
    u = np.zeros((5, 5, 5), dtype=np.float64)
    v = np.zeros((5, 5, 5), dtype=np.float64)
    w = np.zeros((5, 5, 5), dtype=np.float64)

    u[2, 2, 2] = 100.0
    v[2, 2, 2] = 100.0
    w[2, 2, 2] = 100.0

    params = WorkflowParams(
        run=PIVRunParams(
            inter_size=(16, 16, 16),
            search_margin=(8, 8, 8),
            step=(16, 16, 16),
            compute_sn=False,
        ),
        postprocess=PostProcessParams(
            median_despike=MedianDespikeParams(
                enabled=True,
                ksize=3,
                threshold=1.0,
            )
        ),
    )

    result = apply_postprocessing(u, v, w=w, params=params, sn=None)

    assert result.u.shape == (5, 5, 5)
    assert result.v.shape == (5, 5, 5)
    assert result.w is not None
    assert result.w.shape == (5, 5, 5)

    assert result.u[2, 2, 2] == 0.0
    assert result.v[2, 2, 2] == 0.0
    assert result.w[2, 2, 2] == 0.0

    print("3D median-despike smoke test passed")
    print("u shape:", result.u.shape)
    print("v shape:", result.v.shape)
    print("w shape:", result.w.shape)
    print("center u/v/w:", result.u[2, 2, 2], result.v[2, 2, 2], result.w[2, 2, 2])


if __name__ == "__main__":
    main()
