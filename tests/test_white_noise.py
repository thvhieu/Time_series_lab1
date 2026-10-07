from src.white_noise import main


def test_white_noise_entrypoint_exists():
    assert callable(main)
