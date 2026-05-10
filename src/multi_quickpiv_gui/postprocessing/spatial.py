"""Spatial post-processing helpers for PIV vector fields."""

from __future__ import annotations

import numpy as np


def median_despike_vector_field(
    u: np.ndarray,
    v: np.ndarray,
    *,
    w: np.ndarray | None = None,
    ksize: int = 3,
    threshold: float = 3.5,
    use_magnitude: bool = True,
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    """Remove vector outliers using a local median filter for 2D or 3D fields."""
    if u.shape != v.shape:
        raise ValueError("u and v must have the same shape.")
    if w is not None and w.shape != u.shape:
        raise ValueError("w must have the same shape as u and v.")

    if u.ndim not in {2, 3}:
        raise ValueError("Median despiking supports only 2D or 3D vector fields.")

    if ksize < 1:
        raise ValueError("Median-despike window size must be at least 1.")
    if ksize % 2 == 0:
        ksize += 1

    half = ksize // 2

    components = [np.asarray(u), np.asarray(v)]
    if w is not None:
        components.append(np.asarray(w))

    clean_components = [component.copy() for component in components]

    pad_width = tuple((half, half) for _ in range(u.ndim))
    padded_components = [
        np.pad(component, pad_width, mode="reflect")
        for component in components
    ]

    for idx in np.ndindex(u.shape):
        window_slices = tuple(slice(i, i + ksize) for i in idx)
        windows = [
            padded_component[window_slices]
            for padded_component in padded_components
        ]

        if use_magnitude:
            window_magnitude = np.sqrt(
                sum(window.astype(np.float64) ** 2 for window in windows)
            )
            median_magnitude = np.median(window_magnitude)
            mad_magnitude = (
                np.median(np.abs(window_magnitude - median_magnitude)) + 1e-9
            )

            current_magnitude = np.sqrt(
                sum(float(component[idx]) ** 2 for component in components)
            )

            replace = current_magnitude > (
                median_magnitude + threshold * mad_magnitude
            )
        else:
            replace = False
            for component, window in zip(components, windows):
                median_component = np.median(window)
                mad_component = np.median(np.abs(window - median_component)) + 1e-9

                if abs(component[idx] - median_component) > (
                    threshold * mad_component
                ):
                    replace = True
                    break

        if replace:
            for clean_component, window in zip(clean_components, windows):
                clean_component[idx] = np.median(window)

    u_clean = clean_components[0]
    v_clean = clean_components[1]
    w_clean = clean_components[2] if w is not None else None

    return u_clean, v_clean, w_clean


def median_despike(
    u: np.ndarray,
    v: np.ndarray,
    *,
    ksize: int = 3,
    threshold: float = 3.5,
    use_magnitude: bool = True,
) -> tuple[np.ndarray, np.ndarray]:
    """Remove outliers using a median filter for a 2D vector field."""
    u_clean, v_clean, _ = median_despike_vector_field(
        u,
        v,
        w=None,
        ksize=ksize,
        threshold=threshold,
        use_magnitude=use_magnitude,
    )
    return u_clean, v_clean


def sn_threshold_filter(
    u: np.ndarray,
    v: np.ndarray,
    sn: np.ndarray,
    *,
    sn_min: float,
    ksize: int = 3,
) -> tuple[np.ndarray, np.ndarray, int]:
    """
    Replace vectors with SN < sn_min using a local median.

    Returns the filtered (u, v) fields and the number of replaced vectors.
    """
    if u.shape != v.shape:
        raise ValueError("u and v must have the same shape.")
    if sn.shape != u.shape:
        raise ValueError(f"SN shape {sn.shape} does not match vector shape {u.shape}.")
    if sn_min <= 0:
        raise ValueError("SN minimum threshold must be greater than 0.")

    if ksize % 2 == 0:
        ksize += 1
    half = ksize // 2

    u_out = u.copy()
    v_out = v.copy()

    mask = sn < sn_min
    n_replaced = int(np.sum(mask))
    if n_replaced == 0:
        return u_out, v_out, 0

    u_pad = np.pad(u, ((half, half), (half, half)), mode="reflect")
    v_pad = np.pad(v, ((half, half), (half, half)), mode="reflect")

    ys, xs = np.where(mask)
    for i, j in zip(ys, xs):
        w_u = u_pad[i:i + ksize, j:j + ksize]
        w_v = v_pad[i:i + ksize, j:j + ksize]
        u_out[i, j] = np.median(w_u)
        v_out[i, j] = np.median(w_v)

    return u_out, v_out, n_replaced