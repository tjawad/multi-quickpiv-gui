"""Parameter form state and builders for the multi_quickPIV GUI."""

from __future__ import annotations

from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk

from multi_quickpiv_gui.workflow.params import (
    MedianDespikeParams,
    PIVRunParams,
    PostProcessParams,
    SNFilterParams,
    WorkflowParams,
)


@dataclass(slots=True)
class ParamsFormState:
    """Tk variable bundle for the full parameter form."""

    intersize_x: tk.StringVar
    intersize_y: tk.StringVar
    intersize_z: tk.StringVar
    search_x: tk.StringVar
    search_y: tk.StringVar
    search_z: tk.StringVar
    step_x: tk.StringVar
    step_y: tk.StringVar
    step_z: tk.StringVar

    compute_sn: tk.BooleanVar
    corr_alg: tk.StringVar

    despike: tk.BooleanVar
    despike_ksize: tk.StringVar
    despike_thr: tk.StringVar

    sn_filter: tk.BooleanVar
    sn_min: tk.StringVar


def create_params_form_state(master: tk.Misc) -> ParamsFormState:
    """Create the Tk variables used by the parameter form."""
    return ParamsFormState(
        intersize_x=tk.StringVar(master=master, value="64"),
        intersize_y=tk.StringVar(master=master, value="64"),
        intersize_z=tk.StringVar(master=master, value="64"),
        search_x=tk.StringVar(master=master, value="128"),
        search_y=tk.StringVar(master=master, value="128"),
        search_z=tk.StringVar(master=master, value="128"),
        step_x=tk.StringVar(master=master, value="32"),
        step_y=tk.StringVar(master=master, value="32"),
        step_z=tk.StringVar(master=master, value="32"),
        compute_sn=tk.BooleanVar(master=master, value=True),
        corr_alg=tk.StringVar(master=master, value="nsqecc"),
        despike=tk.BooleanVar(master=master, value=False),
        despike_ksize=tk.StringVar(master=master, value="3"),
        despike_thr=tk.StringVar(master=master, value="3.5"),
        sn_filter=tk.BooleanVar(master=master, value=False),
        sn_min=tk.StringVar(master=master, value="1.0"),
    )


def build_params_panel(parent: ttk.Frame, form: ParamsFormState) -> None:
    """Build the full parameter panel into the given parent frame."""
    piv_frame = ttk.LabelFrame(parent, text="PIV Parameters", padding=8)
    piv_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    ttk.Label(piv_frame, text="").grid(row=0, column=0, sticky="w")
    ttk.Label(piv_frame, text="X").grid(row=0, column=1)
    ttk.Label(piv_frame, text="Y").grid(row=0, column=2)
    ttk.Label(piv_frame, text="Z").grid(row=0, column=3)

    ttk.Label(piv_frame, text="interSize").grid(row=1, column=0, sticky="w")
    ttk.Entry(
        piv_frame, width=8, textvariable=form.intersize_x
    ).grid(row=1, column=1, padx=4)
    ttk.Entry(
        piv_frame, width=8, textvariable=form.intersize_y
    ).grid(row=1, column=2, padx=4)
    ttk.Entry(
        piv_frame, width=8, textvariable=form.intersize_z
    ).grid(row=1, column=3, padx=4)

    ttk.Label(piv_frame, text="searchMargin").grid(
        row=2, column=0, sticky="w"
    )
    ttk.Entry(
        piv_frame, width=8, textvariable=form.search_x
    ).grid(row=2, column=1, padx=4)
    ttk.Entry(
        piv_frame, width=8, textvariable=form.search_y
    ).grid(row=2, column=2, padx=4)
    ttk.Entry(
        piv_frame, width=8, textvariable=form.search_z
    ).grid(row=2, column=3, padx=4)

    ttk.Label(piv_frame, text="step").grid(row=3, column=0, sticky="w")
    ttk.Entry(
        piv_frame, width=8, textvariable=form.step_x
    ).grid(row=3, column=1, padx=4)
    ttk.Entry(
        piv_frame, width=8, textvariable=form.step_y
    ).grid(row=3, column=2, padx=4)
    ttk.Entry(
        piv_frame, width=8, textvariable=form.step_z
    ).grid(row=3, column=3, padx=4)

    ttk.Label(
        piv_frame,
        text="Z is used only for 3D PIV",
    ).grid(row=4, column=0, columnspan=4, sticky="w", pady=(6, 0))

    ttk.Checkbutton(
        piv_frame,
        text="computeSN",
        variable=form.compute_sn,
    ).grid(row=5, column=0, sticky="w", pady=(8, 0))

    ttk.Label(piv_frame, text="corr_alg").grid(row=6, column=0, sticky="w")
    corr_alg_combo = ttk.Combobox(
        piv_frame,
        textvariable=form.corr_alg,
        values=("nsqecc", "zncc", "fft"),
        width=12,
        state="normal",
    )
    corr_alg_combo.grid(row=6, column=1, columnspan=3, sticky="ew", pady=4)

    filt_frame = ttk.LabelFrame(parent, text="Median Filter", padding=8)
    filt_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))

    ttk.Checkbutton(
        filt_frame,
        text="Enable median despike",
        variable=form.despike,
    ).grid(row=0, column=0, columnspan=3, sticky="w")

    ttk.Label(filt_frame, text="Window size").grid(row=1, column=0, sticky="w")
    ttk.Entry(
        filt_frame, width=8, textvariable=form.despike_ksize
    ).grid(row=1, column=1, padx=4, pady=4)

    ttk.Label(filt_frame, text="Threshold (MAD ×)").grid(
        row=2, column=0, sticky="w"
    )
    ttk.Entry(
        filt_frame, width=8, textvariable=form.despike_thr
    ).grid(row=2, column=1, padx=4, pady=4)

    sn_frame = ttk.LabelFrame(parent, text="SN Filter", padding=8)
    sn_frame.grid(row=2, column=0, sticky="ew")

    ttk.Checkbutton(
        sn_frame,
        text="Enable SN filtering",
        variable=form.sn_filter,
    ).grid(row=0, column=0, columnspan=2, sticky="w")

    ttk.Label(sn_frame, text="SN minimum").grid(row=1, column=0, sticky="w")
    ttk.Entry(
        sn_frame, width=8, textvariable=form.sn_min
    ).grid(row=1, column=1, padx=4, pady=4)


def _read_int(var: tk.Variable, field_name: str) -> int:
    """Read an integer value from a Tk variable."""
    try:
        return int(var.get())
    except Exception as exc:
        raise ValueError(f"Invalid integer for {field_name}.") from exc


def _read_float(var: tk.Variable, field_name: str) -> float:
    """Read a float value from a Tk variable."""
    try:
        return float(var.get())
    except Exception as exc:
        raise ValueError(f"Invalid float for {field_name}.") from exc


def build_workflow_params(
    form: ParamsFormState,
    *,
    spatial_ndim: int = 2,
) -> WorkflowParams:
    """Build and validate WorkflowParams from the parameter form state."""
    if spatial_ndim not in {2, 3}:
        raise ValueError("spatial_ndim must be 2 or 3.")

    inter_x = _read_int(form.intersize_x, "interSize X")
    inter_y = _read_int(form.intersize_y, "interSize Y")
    inter_z = _read_int(form.intersize_z, "interSize Z")

    search_x = _read_int(form.search_x, "searchMargin X")
    search_y = _read_int(form.search_y, "searchMargin Y")
    search_z = _read_int(form.search_z, "searchMargin Z")

    step_x = _read_int(form.step_x, "step X")
    step_y = _read_int(form.step_y, "step Y")
    step_z = _read_int(form.step_z, "step Z")

    if spatial_ndim == 2:
        inter_size = (inter_y, inter_x)
        search_margin = (search_y, search_x)
        step = (step_y, step_x)
    else:
        inter_size = (inter_z, inter_y, inter_x)
        search_margin = (search_z, search_y, search_x)
        step = (step_z, step_y, step_x)

    params = WorkflowParams(
        run=PIVRunParams(
            inter_size=inter_size,
            search_margin=search_margin,
            step=step,
            compute_sn=bool(form.compute_sn.get()),
            corr_alg=str(form.corr_alg.get()).strip() or "nsqecc",
        ),
        postprocess=PostProcessParams(
            median_despike=MedianDespikeParams(
                enabled=bool(form.despike.get()),
                ksize=max(3, _read_int(form.despike_ksize, "median ksize")),
                threshold=_read_float(form.despike_thr, "median threshold"),
            ),
            sn_filter=SNFilterParams(
                enabled=bool(form.sn_filter.get()),
                minimum=(
                    _read_float(form.sn_min, "SN minimum")
                    if form.sn_filter.get()
                    else 1.0
                ),
            ),
        ),
    )
    params.validate()
    return params