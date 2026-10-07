"""Người 6: chạy tuần tự các module độc lập."""

from pathlib import Path
import subprocess
import sys

SCRIPTS = [
    "data_quality.py",
    "acf_pacf.py",
    "white_noise.py",
    "decomposition.py",
    "visualization.py",
]


def main() -> None:
    src_dir = Path(__file__).resolve().parent
    for name in SCRIPTS:
        path = src_dir / name
        subprocess.run([sys.executable, str(path)], check=True)
        print(f"PASSED: {name}")


if __name__ == "__main__":
    main()
