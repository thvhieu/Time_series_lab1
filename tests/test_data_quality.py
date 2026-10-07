from src.data_quality import main


def test_data_quality_entrypoint_exists():
    assert callable(main)
