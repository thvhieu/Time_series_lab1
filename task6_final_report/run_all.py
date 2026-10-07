"""Người 6: chạy tuần tự năm task độc lập."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "task1_acf_pacf" / "main.py",
    ROOT / "task2_white_noise" / "main.py",
    ROOT / "task3_decomposition" / "main.py",
    ROOT / "task4_data_quality" / "main.py",
    ROOT / "task5_visualization" / "main.py",
]


def main() -> None:
    for script in SCRIPTS:
        subprocess.run([sys.executable, str(script)], check=True)
        print(f"PASSED: {script.parent.name}")


if __name__ == "__main__":
    main()
