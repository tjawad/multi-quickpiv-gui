"""Run project smoke tests."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


QUICK_TESTS = [
    "scripts/smoke_test_params_mapping.py",
    "scripts/smoke_test_3d_tiff_sequence_loading.py",
    "scripts/smoke_test_3d_median_despike.py",
]

JULIA_TESTS = [
    "scripts/smoke_test_3d_bridge.py",
    "scripts/smoke_test_3d_batch_export.py",
]


def run_script(path: Path) -> None:
    """Run one smoke-test script with the current Python interpreter."""
    print()
    print("=" * 80)
    print(f"Running: {path}")
    print("=" * 80)

    subprocess.run(
        [sys.executable, str(path)],
        check=True,
    )


def main() -> None:
    """Run selected smoke tests."""
    parser = argparse.ArgumentParser(description="Run smoke tests.")
    parser.add_argument(
        "--include-julia",
        action="store_true",
        help="Also run slower smoke tests that initialize Julia.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]

    tests = list(QUICK_TESTS)
    if args.include_julia:
        tests.extend(JULIA_TESTS)

    for test in tests:
        run_script(repo_root / test)

    print()
    print("All selected smoke tests passed.")


if __name__ == "__main__":
    main()
