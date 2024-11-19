import os
import tempfile
from typing import Generator

import pytest  # type: ignore

from licesenser.license_manager.get_project_license import (FileFinder,
                                                            LicenseFinder)
from tests.data.mock_data import (empty_license, invalid_file_content,
                                  invalid_licenses,
                                  mock_directory_invalid_structure,
                                  mock_directory_valid_structure,
                                  valid_licenses)


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


# Test setup
@pytest.fixture
def root_directory() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def file_finder() -> FileFinder:
    return FileFinder()


@pytest.fixture
def license_finder(file_finder: FileFinder) -> LicenseFinder:
    return LicenseFinder(file_finder)


@pytest.fixture
def root_directory_valid() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        for file_name, content in mock_directory_valid_structure.items():
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, "w") as f:
                f.write(content)
        yield temp_dir


@pytest.fixture
def root_directory_invalid() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        for file_name, content in mock_directory_invalid_structure.items():
            file_path = os.path.join(temp_dir, file_name)
            with open(file_path, "w") as f:
                f.write(content)
        yield temp_dir


@pytest.fixture
def known_license_text() -> list[str]:
    return valid_licenses


@pytest.fixture
def unknown_license_text() -> list[str]:
    return invalid_licenses


@pytest.fixture
def empty_license_text() -> list[str]:
    return empty_license


@pytest.fixture
def invalid_file_text() -> list[str]:
    return invalid_file_content
