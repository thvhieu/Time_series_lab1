from src.decomposition import main


def test_decomposition_entrypoint_exists():
    assert callable(main)
