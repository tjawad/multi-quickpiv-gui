import numpy as np

from multi_quickpiv_gui.backend.julia_bridge import run_piv_3d

rng = np.random.default_rng(0)

img1 = rng.random((48, 48, 48))
img2 = np.roll(img1, shift=1, axis=2)

result = run_piv_3d(
    img1,
    img2,
    inter_size=(16, 16, 16),
    search_margin=(8, 8, 8),
    step=(16, 16, 16),
    compute_sn=False,
    corr_alg="nsqecc",
)

print("u:", result.u.shape)
print("v:", result.v.shape)
print("w:", None if result.w is None else result.w.shape)
print("xg:", result.xg.shape)
print("yg:", result.yg.shape)
print("zg:", None if result.zg is None else result.zg.shape)
print("sn:", result.sn)
print("mean u/v/w:", result.u.mean(), result.v.mean(), result.w.mean())


