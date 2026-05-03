"""Smoke test for GUI parameter mapping into backend tuple order."""

from __future__ import annotations

import tkinter as tk

from multi_quickpiv_gui.gui.params_form import (
    build_workflow_params,
    create_params_form_state,
)


def main() -> None:
    """Check that GUI X/Y/Z values map to backend tuple order correctly."""
    root = tk.Tk()
    root.withdraw()

    try:
        form = create_params_form_state(root)

        form.intersize_x.set("10")
        form.intersize_y.set("20")
        form.intersize_z.set("30")

        form.search_x.set("11")
        form.search_y.set("21")
        form.search_z.set("31")

        form.step_x.set("12")
        form.step_y.set("22")
        form.step_z.set("32")

        params_2d = build_workflow_params(form, spatial_ndim=2)
        params_3d = build_workflow_params(form, spatial_ndim=3)

        assert params_2d.run.inter_size == (20, 10)
        assert params_2d.run.search_margin == (21, 11)
        assert params_2d.run.step == (22, 12)

        assert params_3d.run.inter_size == (30, 20, 10)
        assert params_3d.run.search_margin == (31, 21, 11)
        assert params_3d.run.step == (32, 22, 12)

        print("Parameter mapping smoke test passed")
        print("2D inter_size:", params_2d.run.inter_size)
        print("2D search_margin:", params_2d.run.search_margin)
        print("2D step:", params_2d.run.step)
        print("3D inter_size:", params_3d.run.inter_size)
        print("3D search_margin:", params_3d.run.search_margin)
        print("3D step:", params_3d.run.step)

    finally:
        root.destroy()


if __name__ == "__main__":
    main()
