import pytest


@pytest.fixture
def temp_dir(tmp_path) -> str:
    """Creates a temporary directory for tests

    Args:
        tmp_path (_type_): tmp_path fixture

    Returns:
        str: tmp_path
    """
    return tmp_path
