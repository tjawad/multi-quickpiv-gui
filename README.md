# multi_quickPIV GUI - 2D PIV with Python and Julia

This project provides a graphical user interface for processing two-dimensional Particle Image Velocimetry (2D PIV) data.

The interface is built with Python and Tkinter. The actual PIV computation is carried out in Julia using the [`multi_quickPIV`](https://github.com/Marc-3d/multi_quickPIV) backend.

The goal of this project is to make `multi_quickPIV` easier to use for users who prefer a visual workflow instead of directly calling the Julia package from code.

The program is currently designed for 2D PIV. An extension to 3D PIV would in principle be possible, but is not currently implemented in this GUI.

## Features

The GUI can load image stacks in TIFF format (`.tif`, `.tiff`) and HDF5 format (`.h5`).

Two main evaluation modes are available:

- **Single PIV**: performs the PIV calculation between one selected frame and the following frame.
- **Batch PIV**: automatically processes all consecutive frame pairs in the loaded image stack.

To improve the quality of the vector fields, optional filtering tools are available:

- median despiking for suppressing outlier vectors
- signal-to-noise filtering, if signal-to-noise values are computed by the backend

During processing, the GUI provides an interactive preview. Individual frames can be viewed, and computed velocity vectors are displayed as a quiver plot over the image data.

The results can be exported as:

- NumPy archive (`.npz`)
- HDF5 file (`.h5`)
- optional video or GIF showing the vector field evolution over time

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
git clone https://github.com/tjawad/multi-quickpiv-gui.git
cd multi-quickpiv-gui
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

A typical workflow is:

1. Start the GUI with `quickpiv-gui`.
2. Load a TIFF or HDF5 image stack.
3. Adjust the PIV parameters if needed.
4. Run a single PIV calculation first to check the result.
5. If the result looks reasonable, run batch PIV.
6. Export the computed vector fields as NPZ/HDF5.
7. Optionally export a video or GIF of the vector fields.

## PIV parameters

The main PIV parameters are:

- **interSize**: size of the interrogation window in pixels.
- **searchMargin**: search area around the interrogation window.
- **step**: spacing between neighboring vectors.
- **computeSN**: enables signal-to-noise computation in the Julia backend.

Smaller steps create denser vector fields but increase computation time. Larger interrogation windows can make the correlation more stable but reduce spatial resolution.

## Smoke test

A command-line smoke test is available, but it requires an input image stack:

```bash
python scripts/smoke_test_pipeline.py path/to/input_stack.tif
```

For batch mode:

```bash
python scripts/smoke_test_pipeline.py path/to/input_stack.tif --mode batch --out test_outputs/batch_result.npz
```

## Project structure

The repository is organized as a Python package:

```text
multi-quickpiv-gui/
|-- src/multi_quickpiv_gui/   # GUI, backend bridge, runtime, and workflow code
|-- julia_env/                # local Julia environment for multi_quickPIV
|-- scripts/                  # helper scripts and smoke tests
|-- docs/                     # documentation material
|-- tests/                    # tests
|-- requirements.txt          # pinned Python dependencies
|-- environment.yml           # portable conda environment
|-- environment-windows-lock.yml
`-- pyproject.toml            # Python package and launcher configuration
```

The Julia backend is managed through the local `julia_env/` directory. This keeps the Julia dependency setup separate from the user's global Julia environment.

## Notes

This GUI is a frontend for `multi_quickPIV`. The Julia backend itself remains a separate Julia-only project.

The GUI currently focuses on 2D PIV workflows. The underlying `multi_quickPIV` backend supports more advanced functionality, but not all backend features are exposed in the GUI yet.

This project is under active development.
