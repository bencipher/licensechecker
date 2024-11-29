# type:ignore
from unittest.mock import MagicMock, patch

import pytest
import requests
from requests import ConnectTimeout

from licesenser.license_manager.get_dependency_license import (
    create_package_info, get_deps_info_from_local, get_deps_info_from_pypi,
    get_license_from_classifier, get_project_packages)

# Mock data for classifiers
mock_classifiers = [
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
]

# Mock data for metadata
mock_metadata = {
    "Name": "example",
    "Version": "1.0.0",
    "Home-page": "https://example.com",
    "Author": "John Doe",
    "Author-email": "john.doe@example.com",
    "License": "MIT License",
    "Classifier": mock_classifiers,
}

# Mock data for PyPI response
mock_pypi_response = {
    "info": {
        "name": "example",
        "version": "1.0.0",
        "home_page": "https://example.com",
        "author": "John Doe",
        "author_email": "john.doe@example.com",
        "license": "MIT License",
        "classifiers": mock_classifiers,
    },
    "urls": [{"size": 1024}],
}


# Mock data for package not found
mock_nonexistent_package = "nonexistent"


class MockMetadata:
    def __init__(self) -> None:
        self.metadata = mock_metadata

    def get_all(self, key):
        return mock_classifiers

    def get(self, key):
        return self.metadata.get(key)


# Test Fixtures


@pytest.fixture
def mock_metadata_distribution():
    # Create a mock distribution object
    mock_distribution = MagicMock()
    mock_distribution.metadata = MockMetadata()  # Use the mock class
    mock_distribution.files = [MagicMock(size=1024)]
    return mock_distribution


@pytest.fixture
def mock_get_deps_info_from_local(mock_metadata_distribution):
    with patch("importlib.metadata.Distribution.from_name") as mock_local_deps:
        mock_local_deps.return_value = mock_metadata_distribution
        yield mock_local_deps


@pytest.fixture
def mock_pypi_response_fixture():
    with patch("licesenser.connections.session.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_pypi_response
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_metadata_distribution_not_found():
    with patch(
        "importlib.metadata.Distribution.from_name", side_effect=ModuleNotFoundError
    ):
        yield


@pytest.fixture(scope="module")
def mock_requirements():
    return {"example==^1.0.1", "nonexistent==0.0.0", "another-example=x.x.x"}


# Test get_license_from_classifier
def test_get_license_from_classifier():
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
    license_str = get_license_from_classifier(classifiers)
    assert (
        license_str
        == "MIT License;; Apache Software License;; GNU General Public License v3 (GPLv3)".upper()
    )


def test_get_license_from_classifier_no_classifiers():
    """Test with an empty list of classifiers, expecting the output to be UNKNOWN"""
    assert get_license_from_classifier([]) == "UNKNOWN"


def test_get_license_from_classifier_no_license():
    """Test with a list of classifiers that does not contain any license strings,
    expecting the output to be UNKNOWN."""
    assert get_license_from_classifier(["Some Classifier"]) == "UNKNOWN"


def test_get_license_from_unsure_osi_classifier():
    """Test with a list of classifiers that might includes "OSI Approved" licenses,
    but no valid or clear license or not tagged as OSI APPROVED."""
    classifiers = [
        "License :: OSI :: MIT License",
        "License :: OSI Approved",
    ]
    result = get_license_from_classifier(classifiers)
    assert result == "UNKNOWN"


# Test create_package_info
def test_create_package_info():
    package_info = create_package_info(
        name="example",
        local_version="1.0.0",
        latest_version="1.0.0",
        homepage="https://example.com",
        author="John Doe",
        author_email="john.doe@example.com",
        size=1024,
        license="MIT License",
    )
    assert package_info.name == "example"
    assert package_info.local_version == "1.0.0"
    assert package_info.latest_version == "1.0.0"
    assert package_info.homepage == "https://example.com"
    assert package_info.author == "John Doe"
    assert package_info.author_email == "john.doe@example.com"
    assert package_info.size == 1024
    assert package_info.license == "MIT License"
    assert package_info.error_code == 0


def test_create_package_info_missing_fields():
    with pytest.raises(ValueError):
        create_package_info(name=None)


def test_create_package_info_default():
    """Test creating a PackageInfo instance with optional parameters
    set to None, ensuring defaults are applied correctly."""
    package_info = create_package_info(name="example")
    assert package_info.local_version == "UNKNOWN"
    assert package_info.latest_version == "UNKNOWN"
    assert package_info.homepage is None
    assert package_info.author is None
    assert package_info.author_email is None
    assert package_info.size == -1
    assert package_info.license == "UNKNOWN"
    assert package_info.error_code == 0


# Test get_deps_info_from_local
def test_get_deps_info_from_local(mock_get_deps_info_from_local):
    package_info = get_deps_info_from_local("example")
    assert package_info.name == "example"
    assert package_info.local_version == "1.0.0"
    assert package_info.homepage == "https://example.com"
    assert package_info.author == "John Doe"
    assert package_info.author_email == "john.doe@example.com"
    assert package_info.size == 1024
    assert (
        package_info.license
        == "MIT License;; Apache Software License;; GNU General Public License v3 (GPLv3)".upper()
    )
    assert package_info.error_code == 0


def test_get_deps_info_from_local_package_not_found():
    with pytest.raises(ModuleNotFoundError):
        get_deps_info_from_local("nonexistent")


def test_get_deps_info_from_local_author_email_format(mock_metadata_distribution):
    """Test retrieving package info with various formats of author email from
    PyPI, ensuring they are parsed correctly"""
    # Mocking a distribution with various author email formats
    with patch(
        "importlib.metadata.Distribution.from_name",
        return_value=mock_metadata_distribution,
    ):
        package_info = get_deps_info_from_local("example")
        assert package_info.author_email == "john.doe@example.com"


# Test get_deps_info_from_pypi
def test_get_deps_info_from_pypi(mock_pypi_response_fixture):
    package_info = get_deps_info_from_pypi("example")
    assert package_info.name == "example"
    assert package_info.latest_version == "1.0.0"
    assert package_info.homepage == "https://example.com"
    assert package_info.author == "John Doe"
    assert package_info.author_email == "john.doe@example.com"
    assert package_info.size == 1024
    assert (
        package_info.license
        == "MIT License;; Apache Software License;; GNU General Public License v3 (GPLv3)".upper()
    )
    assert package_info.error_code == 0


def test_get_deps_info_from_pypi_package_not_found():
    with patch("licesenser.connections.session.get", side_effect=ConnectTimeout):
        with pytest.raises(ModuleNotFoundError):
            get_deps_info_from_pypi("nonexistent")


def test_get_deps_info_from_pypi_timeout():
    """Test retrieving package info from PyPI when a timeout occurs, expecting a
    ModuleNotFoundError to be raised."""
    with patch(
        "licesenser.connections.session.get",
        side_effect=requests.exceptions.ConnectionError,
    ):
        with pytest.raises(ModuleNotFoundError):
            get_deps_info_from_pypi("example")


def test_get_deps_info_from_pypi_invalid_json():
    """Test retrieving package info from PyPI when the response is not valid JSON,
    ensuring the error is handled gracefully"""
    with patch("licesenser.connections.session.get", side_effect=KeyError):
        with pytest.raises(ModuleNotFoundError):
            get_deps_info_from_pypi("example")


def test_get_deps_info_from_pypi_missing_fields():
    """Test retrieving package info from PyPI when certain fields are missing
    in the response, ensuring defaults are applied correctly"""
    mock_pypi_response["info"].pop("author_email")  # Simulate missing field
    with patch("licesenser.connections.session.get") as mock_get:
        mock_get.return_value.json.return_value = mock_pypi_response
        package_info = get_deps_info_from_pypi("example")
        assert package_info.author_email is None  # Should be None if missing


def test_get_deps_info_from_pypi_author_email_format():
    """Test retrieving package info with various formats of author
    email from PyPI, ensuring they are parsed correctly"""
    mock_pypi_response["info"]["author_email"] = "John Doe <john.doe@example.com>"
    with patch("licesenser.connections.session.get") as mock_get:
        mock_get.return_value.json.return_value = mock_pypi_response
        package_info = get_deps_info_from_pypi("example")
        assert package_info.author_email == "john.doe@example.com"


def test_get_project_packages_ignore_python():
    """Test retrieving package info when 'python' is included in the requirements,
    ensuring it is ignored."""
    mock_requirements_with_python = {"python", "example"}
    package_info_set = get_project_packages(mock_requirements_with_python)
    assert all(pkg.name != "python" for pkg in package_info_set)


def test_get_project_packages_missing_packages():
    """Test retrieving package info when some packages do not exist,
    ensuring they are handled gracefully."""
    mock_requirements_with_nonexistent = {"example", "nonexistent"}
    package_info_set = get_project_packages(mock_requirements_with_nonexistent)
    assert len(package_info_set) == 2  # Should include example and handle nonexistent


# Integration Tests
# Test get_project_packages
@pytest.mark.skip("Integration tests")
def test_get_project_packages():
    package_info_set = get_project_packages(mock_requirements)
    assert len(package_info_set) == 3

    # Check for the "example" package
    example_package = next(
        (pkg for pkg in package_info_set if pkg.name == "EXAMPLE"), None
    )
    assert example_package is not None
    assert example_package.local_version == "1.0.0"
    assert example_package.latest_version == "1.0.0"
    assert example_package.homepage == "https://example.com"
    assert example_package.author == "John Doe"
    assert example_package.author_email == "john.doe@example.com"
    assert example_package.size == 1024
    assert (
        example_package.license
        == "MIT License, Apache Software License, GNU General Public License v3 (GPLv3)"
    )
    assert example_package.error_code == 0

    # Check for the "nonexistent" package
    nonexistent_package = next(
        (pkg for pkg in package_info_set if pkg.name == "NONEXISTENT"), None
    )
    assert nonexistent_package is not None
    assert nonexistent_package.local_version == "UNKNOWN"
    assert nonexistent_package.latest_version == "UNKNOWN"
    assert nonexistent_package.homepage is None
    assert nonexistent_package.author is None
    assert nonexistent_package.author_email is None
    assert nonexistent_package.size == -1
    assert nonexistent_package.license == "UNKNOWN"
    assert nonexistent_package.error_code == 1

    # Check for the "another-example" package
    another_example_package = next(
        (pkg for pkg in package_info_set if pkg.name == "ANOTHER-EXAMPLE"), None
    )
    assert another_example_package is not None
    assert another_example_package.local_version == "UNKNOWN"
    assert another_example_package.latest_version == "UNKNOWN"
    assert another_example_package.homepage is None
    assert another_example_package.author is None
    assert another_example_package.author_email is None
    assert another_example_package.size == -1
    assert another_example_package.license == "UNKNOWN"
    assert another_example_package.error_code == 1


# Test get_project_packages with local and PyPI failures
@pytest.mark.skip()
def test_get_project_packages_local_failure_pypi_success(
    mock_requirements, mock_metadata_distribution_not_found, mock_pypi_response_fixture
):
    """Test retrieving package info where some packages are
    found locally and others are fetched from PyPI."""
    package_info_set = get_project_packages(mock_requirements)
    assert len(package_info_set) == 3

    # Check for the "example" package
    example_package = next(
        (pkg for pkg in package_info_set if pkg.name == "EXAMPLE"), None
    )
    assert example_package is not None
    assert example_package.local_version == "UNKNOWN"
    assert example_package.latest_version == "1.0.0"
    assert example_package.homepage == "https://example.com"
    assert example_package.author == "John Doe"
    assert example_package.author_email == "john.doe@example.com"
    assert example_package.size == 1024
    assert (
        example_package.license
        == "MIT License, Apache Software License, GNU General Public License v3 (GPLv3)"
    )
    assert example_package.error_code == 0


@pytest.mark.skip()
def test_get_project_packages_with_invalid_reqs():
    """Test retrieving package info with invalid requirement formats,
    ensuring they are ignored or handled gracefully"""
    mock_requirements_with_invalid = {"example", "invalid==format"}
    package_info_set = get_project_packages(mock_requirements_with_invalid)
    assert len(package_info_set) == 1  # Should only include valid example package
