# multi_quickPIV GUI - 2D and export-only 3D PIV with Python and Julia

This project provides a graphical user interface for processing Particle Image Velocimetry (PIV) data using the Julia [`multi_quickPIV`](https://github.com/Marc-3d/multi_quickPIV) backend.

The GUI currently supports:

- **2D PIV** with image/vector preview, single-pair analysis, batch analysis, post-processing, and export.
- **3D PIV** as an experimental export-only workflow for time-series volume data.

The interface is built with Python and Tkinter. The actual PIV computation is carried out in Julia using the [`multi_quickPIV`](https://github.com/Marc-3d/multi_quickPIV) backend.

The goal of this project is to make `multi_quickPIV` easier to use for users who prefer a visual workflow instead of directly calling the Julia package from code.

3D PIV support is currently focused on batch computation and export. The GUI intentionally does not preview or visualize 3D image volumes or 3D vector fields.

## Features

The GUI can load PIV input data in TIFF format (`.tif`, `.tiff`) and HDF5 format (`.h5`).

Supported input formats are:

- **2D PIV time series**: a stack shaped as `(T, H, W)`, where `T` is time/frame index.
- **3D PIV time series**: a stack shaped as `(T, Z, Y, X)`.
- **Separate 3D TIFF time points**: multiple TIFF files where each file is one 3D volume shaped as `(Z, Y, X)`. These are internally stacked as `(T, Z, Y, X)`.

Two main 2D evaluation modes are available:

- **Single PIV**: performs the PIV calculation between one selected frame and the following frame.
- **Batch PIV**: automatically processes all consecutive frame pairs in the loaded image stack.

For 3D PIV, the GUI supports:

- loading a single 4D HDF5/TIFF stack
- loading multiple 3D TIFF time-point files
- running export-only batch 3D PIV
- exporting `U`, `V`, `W`, `xgrid`, `ygrid`, and `zgrid`

To improve vector fields, optional filtering tools are available:

- median despiking for 2D and 3D vector fields
- signal-to-noise filtering for 2D PIV only

During 2D processing, the GUI provides an interactive preview. Individual frames can be viewed, and computed velocity vectors are displayed as a quiver plot over the image data.

3D processing is export-only. The GUI does not display 3D image data or 3D vector fields.

The results can be exported as:

- NumPy archive (`.npz`)
- HDF5 file (`.h5`)
- optional video or GIF for 2D batch vector-field evolution

## Requirements

To use the GUI, you need:

- Git
- Conda or Miniconda
- Python 3.10
- Julia
- a working terminal or command prompt

Julia must be available from the terminal. You can check this with:

```bash
julia -v
```

For MP4 video export, a working FFmpeg installation is useful. If FFmpeg is not available, GIF export can be used instead.

## Installation

Clone the repository:

```bash
git clone https://github.com/tjawad/multi_quickPIV_GUI.git
cd multi_quickPIV_GUI
```

Create the Python environment:

```bash
conda env create -f environment.yml
conda activate quickpiv
```

Install the GUI package in editable mode:

```bash
pip install -e .
```

Bind PyJulia/PyCall to the active Python environment:

```bash
python -c "import julia; julia.install()"
```

This step is important because the Python GUI communicates with the Julia backend through PyJulia.

## Launching the GUI

After installation, the GUI can be started with:

```bash
quickpiv-gui
```

On first launch, Julia may instantiate the local Julia environment and install `multi_quickPIV` if needed. This can take some time. Later launches should be faster.

## Exact Windows environment

The default `environment.yml` is intended to be portable and should be used by most users.

For reproducing the original tested Windows setup more exactly, use:

```bash
conda env create -f environment-windows-lock.yml
conda activate quickpiv
pip install -e .
python -c "import julia; julia.install()"
quickpiv-gui
```

## Basic workflow

### 2D PIV workflow

A typical 2D workflow is:

1. Start the GUI with `quickpiv-gui`.
2. Select **Load file for 2D PIV**.
3. Load a TIFF or HDF5 image stack shaped as `(T, H, W)`.
4. Adjust the PIV parameters if needed.
5. Run a single PIV calculation first to check the result.
6. If the result looks reasonable, run batch PIV.
7. Export the computed vector fields as NPZ/HDF5.
8. Optionally export a video or GIF of the 2D vector fields.

### 3D PIV workflow

A typical 3D workflow is:

1. Start the GUI with `quickpiv-gui`.
2. Select **Load file for 3D PIV**.
3. Load either:
   - one 4D HDF5/TIFF stack shaped as `(T, Z, Y, X)`, or
   - multiple 3D TIFF time-point files, each shaped as `(Z, Y, X)`.
4. Adjust the PIV parameters if needed.
5. Run batch PIV.
6. Choose the export format, either NPZ or HDF5.
7. Export the 3D vector fields.

3D PIV is currently export-only. No 3D preview, 3D vector-field visualization, or video/GIF export is provided.

## PIV parameters

The main PIV parameters are:

- **interSize**: size of the interrogation window in pixels.
- **searchMargin**: search area around the interrogation window.
- **step**: spacing between neighboring vectors.
- **computeSN**: enables signal-to-noise computation in the Julia backend.

The GUI displays spatial parameters in user-facing order:

```text
X, Y, Z
```

Internally, these are converted to the array order expected by the backend:

```text
2D PIV:
  backend order = (Y, X)

3D PIV:
  backend order = (Z, Y, X)
```

For 2D PIV, the `Z` parameter field is ignored.

Smaller steps create denser vector fields but increase computation time. Larger interrogation windows can make the correlation more stable but reduce spatial resolution.

### 3D signal-to-noise limitation

At present, `computeSN` and signal-to-noise filtering are disabled in 3D mode.

This is because 3D `computeSN=true` currently triggers a backend error inside `multi_quickPIV.compute_SN`. The GUI therefore forces `computeSN=False` for 3D PIV until the backend issue is resolved.

Median despiking remains available for 3D vector fields.

## Smoke test

A command-line smoke test is available, but it requires an input image stack.

The repository does not include large test image stacks. To run the smoke test, place your own `.tif`, `.tiff`, or `.h5` stack somewhere locally, for example in a local `test_data/` folder.

The `test_data/` folder is ignored by Git so that large microscopy files are not accidentally committed.

For a single frame pair:

```bash
python scripts/smoke_test_pipeline.py test_data/example_stack.h5 --mode single --frame-index 0 --out test_outputs/example_single_result.npz
```

For a full batch run:

```bash
python scripts/smoke_test_pipeline.py test_data/example_stack.h5 --mode batch --out test_outputs/example_batch_result.npz
```

The output format is selected by the file extension passed to `--out`. Use `.npz` for a NumPy archive or `.h5` for HDF5 output.

Additional smoke tests are available for the 3D development path:

```bash
python scripts/smoke_test_3d_bridge.py
python scripts/smoke_test_3d_batch_export.py
python scripts/smoke_test_3d_median_despike.py
python scripts/smoke_test_params_mapping.py
python scripts/smoke_test_3d_tiff_sequence_loading.py
```

A smoke-test runner is also available:

```bash
python scripts/run_smoke_tests.py
```

By default, this runs the lightweight Python-only smoke tests.

To also run the Julia-backed smoke tests, use:

```bash
python scripts/run_smoke_tests.py --include-julia
```

The Julia-backed tests initialize the Julia runtime and may take longer to run.

These tests check:

- Python-to-Julia 3D PIV bridge behavior
- 3D batch export/reload behavior
- 3D median despiking
- GUI parameter mapping from `X, Y, Z` to backend tuple order
- loading separate 3D TIFF volumes as a time series

## 3D real-data validation

The 3D workflow has been locally validated using cropped time-point volumes from the Pereyra/QuickPIV example dataset.

The validation input was a cropped HDF5 stack with shape:

```text
(T, Z, Y, X) = (2, 128, 256, 256)
```

The validation checked the following path:

```text
load 3D stack
→ run 3D batch PIV
→ apply 3D median despike
→ export NPZ
→ reload NPZ
→ export HDF5
→ reload HDF5
```

The resulting vector-field shapes were:

```text
Per frame pair:
  U, V, W: (4, 8, 8)

Batch export:
  U, V, W: (1, 4, 8, 8)

Grids:
  xgrid, ygrid, zgrid: (4, 8, 8)

SN:
  None, as expected for 3D mode
```

The cropped validation data are not included in the repository because microscopy datasets are large and the `test_data/` folder is intentionally ignored by Git.

## Project structure

The repository is organized as a Python package:

```text
multi_quickPIV_GUI/
|-- src/multi_quickpiv_gui/   # GUI, backend bridge, runtime, and workflow code
|-- julia_env/                # local Julia environment for multi_quickPIV
|-- scripts/                  # helper scripts and smoke tests
|-- requirements.txt          # Python dependencies
|-- environment.yml           # portable conda environment
|-- environment-windows-lock.yml
|-- pyproject.toml            # Python package and launcher configuration
`-- README.md
```

The Julia backend is managed through the local `julia_env/` directory. This keeps the Julia dependency setup separate from the user's global Julia environment.

## Notes

This GUI is a frontend for `multi_quickPIV`. The Julia backend itself remains a separate Julia-only project.

The GUI supports 2D PIV as the main interactive workflow. The 3D PIV workflow is currently experimental and export-only.

Currently intentional 3D limitations:

- no 3D image preview
- no 3D vector-field preview
- no saved 3D result viewing
- no 3D video/GIF export
- no 3D signal-to-noise computation or SN filtering until the backend issue is resolved

This project is under active development.
