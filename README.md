# multi_quickPIV GUI

A Python/Tkinter graphical user interface for running 2D PIV analysis with the Julia [`multi_quickPIV`](https://github.com/Marc-3d/multi_quickPIV) backend.

The GUI is intended to make `multi_quickPIV` easier to use for users who prefer a visual workflow instead of calling the Julia backend directly.

## Current status

This project is under active development.

Currently supported:

- loading TIFF/TIF and HDF5 image stacks
- previewing image frames
- running single-frame-pair PIV
- running batch PIV
- optional median despiking
- optional signal-to-noise filtering
- exporting PIV results as NPZ/HDF5
- optional video/GIF export

The current GUI is focused on 2D PIV.

## Requirements

You need:

- Git
- Conda or Miniconda
- Julia
- Python 3.10

Julia must be available from the terminal:

```bash
julia -v
```

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

## Launch the GUI

After installation, launch the GUI with:

```bash
quickpiv-gui
```

## Exact Windows environment

The default `environment.yml` is intended to be portable.

For reproducing the original tested Windows setup more exactly, use:

```bash
conda env create -f environment-windows-lock.yml
conda activate quickpiv
pip install -e .
python -c "import julia; julia.install()"
quickpiv-gui
```

## Basic workflow

1. Start the GUI with `quickpiv-gui`.
2. Load a `.tif`, `.tiff`, or `.h5` image stack.
3. Adjust PIV parameters if needed.
4. Run a single PIV test first.
5. If the result looks reasonable, run batch PIV.
6. Export results as NPZ/HDF5.

## Smoke test

A command-line smoke test is available, but it requires an input image stack:

```bash
python scripts/smoke_test_pipeline.py path/to/input_stack.tif
```

For batch mode:

```bash
python scripts/smoke_test_pipeline.py path/to/input_stack.tif --mode batch --out test_outputs/batch_result.npz
```

## Notes

The Julia backend is managed through the local `julia_env/` directory. On first launch, Julia may instantiate the environment and install `multi_quickPIV` if needed. This can take some time.

MP4 export may require FFmpeg. If FFmpeg is unavailable, GIF export can be used instead.