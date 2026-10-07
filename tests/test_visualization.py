from src.visualization import main


def test_visualization_entrypoint_exists():
    assert callable(main)
