import tempfile
from pathlib import Path

import numpy as np

from multi_quickpiv_gui.workflow.params import PIVRunParams, WorkflowParams
from multi_quickpiv_gui.workflow.pipeline import run_batch_piv
from multi_quickpiv_gui.backend.export import save_batch_result
from multi_quickpiv_gui.backend.io import load_saved_piv_result

rng = np.random.default_rng(0)

# Synthetic 3D time series: (T, Z, Y, X)
frame0 = rng.random((48, 48, 48))
frame1 = np.roll(frame0, shift=1, axis=2)
frame2 = np.roll(frame1, shift=1, axis=2)

stack = np.stack([frame0, frame1, frame2])

params = WorkflowParams(
    run=PIVRunParams(
        inter_size=(16, 16, 16),
        search_margin=(8, 8, 8),
        step=(16, 16, 16),
        compute_sn=False,
        corr_alg="nsqecc",
    )
)

batch = run_batch_piv(stack, params=params)

print("pair count:", len(batch.pair_results))
print("batch U fields:", [u.shape for u in batch.u_list])
print("batch V fields:", [v.shape for v in batch.v_list])
print("batch W fields:", None if batch.w_list is None else [w.shape for w in batch.w_list])
print("batch xg:", None if batch.xg is None else batch.xg.shape)
print("batch yg:", None if batch.yg is None else batch.yg.shape)
print("batch zg:", None if batch.zg is None else batch.zg.shape)

with tempfile.TemporaryDirectory() as tmp:
    out_path = Path(tmp) / "batch_3d_test.npz"

    saved = save_batch_result(out_path, batch)
    loaded = load_saved_piv_result(saved.path)

    print("saved:", saved.path.name)
    print("loaded U:", loaded.u.shape)
    print("loaded V:", loaded.v.shape)
    print("loaded W:", None if loaded.w is None else loaded.w.shape)
    print("loaded xgrid:", loaded.xg.shape)
    print("loaded ygrid:", loaded.yg.shape)
    print("loaded zgrid:", None if loaded.zg is None else loaded.zg.shape)
    print("loaded SN:", loaded.sn)

    assert loaded.u.shape == (2, 3, 3, 3)
    assert loaded.v.shape == (2, 3, 3, 3)
    assert loaded.w is not None
    assert loaded.w.shape == (2, 3, 3, 3)

    assert loaded.xg.shape == (3, 3, 3)
    assert loaded.yg.shape == (3, 3, 3)
    assert loaded.zg is not None
    assert loaded.zg.shape == (3, 3, 3)

print("3D batch/export/reload smoke test passed")

