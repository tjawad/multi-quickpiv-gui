"""Post-processing pipeline orchestration for computed PIV vector fields."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from multi_quickpiv_gui.postprocessing.spatial import (
    median_despike_vector_field,
    sn_threshold_filter,
)
from multi_quickpiv_gui.workflow.params import WorkflowParams


@dataclass(slots=True)
class PostProcessResult:
    """Processed vector field plus metadata about the applied filters."""

    u: np.ndarray
    v: np.ndarray
    w: np.ndarray | None = None
    sn: np.ndarray | None = None
    sn_replaced: int = 0


def apply_postprocessing(
    u: np.ndarray,
    v: np.ndarray,
    *,
    params: WorkflowParams,
    sn: np.ndarray | None = None,
    w: np.ndarray | None = None,
) -> PostProcessResult:
    """
    Apply all configured post-processing steps to a computed vector field.
    """
    params.validate()

    if u.shape != v.shape:
        raise ValueError("u and v must have the same shape.")

    if w is not None and w.shape != u.shape:
        raise ValueError("w must have the same shape as u and v.")

    u_out = np.asarray(u, dtype=np.float64).copy()
    v_out = np.asarray(v, dtype=np.float64).copy()
    w_out = None if w is None else np.asarray(w, dtype=np.float64).copy()
    sn_out = None if sn is None else np.asarray(sn, dtype=np.float64).copy()

    post = params.postprocess

    if post.median_despike.enabled:
        u_out, v_out, w_out = median_despike_vector_field(
            u_out,
            v_out,
            w=w_out,
            ksize=post.median_despike.ksize,
            threshold=post.median_despike.threshold,
            use_magnitude=True,
        )

    sn_replaced = 0
    if post.sn_filter.enabled:
        if w_out is not None:
            raise ValueError("SN filtering is not implemented for 3D vector fields yet.")

        if sn_out is None:
            raise ValueError(
                "SN filtering is enabled, but no SN array was provided."
            )

        u_out, v_out, sn_replaced = sn_threshold_filter(
            u_out,
            v_out,
            sn_out,
            sn_min=post.sn_filter.minimum,
            ksize=post.median_despike.ksize,
        )

    return PostProcessResult(
        u=u_out,
        v=v_out,
        w=w_out,
        sn=sn_out,
        sn_replaced=sn_replaced,
    )