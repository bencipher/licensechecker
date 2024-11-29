# type: ignore
from unittest.mock import MagicMock, patch

import pytest

from licesenser.license_manager.get_dependency_license import \
    get_deps_info_from_local


class MockMetadata:
    def __init__(self) -> None:
        self.metadata = {
            "Name": "example",
            "Version": "1.0.0",
            "Home-page": "https://example.com",
            "Author": "John Doe",
            "Author-email": "john.doe@example.com",
            "License": "MIT License",
            "Classifier": [],
        }

    def get_all(self, key):
        return ["License :: OSI Approved :: MIT License"]

    def get(self, key):
        return self.metadata.get(key)


@pytest.fixture
def mock_metadata_distribution():
    # Create a mock distribution object
    mock_distribution = MagicMock()
    mock_distribution.metadata = MockMetadata()  # Use the mock class
    mock_distribution.files = [MagicMock(size=1024)]
    return mock_distribution


def test_get_deps_info_from_local(mock_metadata_distribution):
    # Patch the importlib.metadata.Distribution.from_name method
    with patch(
        "licesenser.license_manager.get_dependency_license.metadata.Distribution.from_name",
        return_value=mock_metadata_distribution,
    ):
        package_info = get_deps_info_from_local("example")

        # Assertions to check if the package info is as expected
        assert package_info.name == "example"
        assert package_info.local_version == "1.0.0"
        assert package_info.homepage == "https://example.com"
        assert package_info.author == "John Doe"
        assert package_info.author_email == "john.doe@example.com"
        assert package_info.size == 1024
        assert package_info.license == "MIT LICENSE"
