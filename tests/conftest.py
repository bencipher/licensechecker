import os

import pytest  # type: ignore


@pytest.fixture(scope="module")
def pipfile_data() -> str:
    return os.path.join(os.path.dirname(__file__), "data", "Pipfile")


@pytest.fixture(scope="module")
def pyproject_data() -> str:
    return os.path.join(os.path.dirname(__file__), "data", "pyproject.toml")


@pytest.fixture(scope="module")
def requirements_data() -> str:
    return os.path.join(os.path.dirname(__file__), "data", "requirements.txt")


@pytest.fixture(scope="module")
def unsupported_data() -> str:
    return os.path.join(os.path.dirname(__file__), "data", "dependencies.json")
