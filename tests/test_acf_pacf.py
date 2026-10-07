from src.acf_pacf import main


def test_acf_pacf_entrypoint_exists():
    assert callable(main)
