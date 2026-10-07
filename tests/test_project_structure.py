from pathlib import Path


def test_required_directories_exist():
    required = ["data/raw", "data/processed", "src", "tests", "artifacts", "reports/sections", "evidence"]
    for path in required:
        assert Path(path).is_dir(), f"Missing directory: {path}"


def test_required_project_files_exist():
    required = ["README.md", "requirements.txt", "src/run_all.py"]
    for path in required:
        assert Path(path).is_file(), f"Missing file: {path}"
