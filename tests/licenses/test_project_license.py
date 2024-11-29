# type:ignore
import os

import pytest  # type: ignore

from licesenser.enums import LicenseType
from licesenser.license_manager.get_project_license import LicenseFinder


# Test functions
def test_find_all_license_information(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    all_license_info = license_finder.find_all_license_information(root_directory_valid)
    assert isinstance(all_license_info, dict)
    for file_path, info in all_license_info.items():
        assert os.path.exists(file_path)
        assert info is not None
        assert info in [
            LicenseType.LGPL,
            LicenseType.MIT,
            LicenseType.UNKNOWN,
        ]


def test_find_first_license_information(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    first_license_info = license_finder.find_first_license_information(
        root_directory_valid
    )
    assert first_license_info is not None
    assert first_license_info in [
        LicenseType.LGPL,
        LicenseType.MIT,
        LicenseType.UNKNOWN,
    ]


@pytest.mark.asyncio
async def test_find_all_license_information_async(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    all_license_info = await license_finder.find_all_license_information_async(
        root_directory_valid
    )
    assert isinstance(all_license_info, dict)
    for file_path, info in all_license_info.items():
        assert os.path.exists(file_path)
        assert info is not None
        assert info in [
            LicenseType.LGPL,
            LicenseType.MIT,
            LicenseType.UNKNOWN,
        ]


@pytest.mark.asyncio
async def test_find_first_license_information_async(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    first_license_info = await license_finder.find_first_license_information_async(
        root_directory_valid
    )
    assert first_license_info is not None
    assert first_license_info in [
        LicenseType.LGPL,
        LicenseType.MIT,
        LicenseType.UNKNOWN,
    ]


def test_empty_license_files(
    license_finder: LicenseFinder, root_directory_invalid: str
) -> None:
    empty_files = [os.path.join(root_directory_invalid, "license")]
    all_license_info = license_finder.find_all_license_information(
        root_directory_invalid
    )
    for file_path in empty_files:
        assert all_license_info.get(file_path) == LicenseType.UNKNOWN


@pytest.mark.asyncio
async def test_empty_license_files_async(
    license_finder: LicenseFinder, root_directory_invalid: str
) -> None:
    empty_files = [os.path.join(root_directory_invalid, "license")]
    all_license_info = await license_finder.find_all_license_information_async(
        root_directory_invalid
    )
    for file_path in empty_files:
        assert all_license_info.get(file_path) == LicenseType.UNKNOWN


def test_non_license_files(
    license_finder: LicenseFinder, root_directory_invalid: str
) -> None:
    invalid_files = [
        os.path.join(root_directory_invalid, "invalid_file_content.txt"),
        os.path.join(root_directory_invalid, "license.apache.rst"),
    ]
    all_license_info = license_finder.find_all_license_information(
        root_directory_invalid
    )
    for file_path in invalid_files:
        assert all_license_info.get(file_path) is None


@pytest.mark.asyncio
async def test_non_license_files_async(
    license_finder: LicenseFinder, root_directory_invalid: str
) -> None:
    invalid_files = [
        os.path.join(root_directory_invalid, "invalid_license.txt"),
        os.path.join(root_directory_invalid, "invalid_license.rst"),
    ]
    all_license_info = await license_finder.find_all_license_information_async(
        root_directory_invalid
    )
    for file_path in invalid_files:
        assert all_license_info.get(file_path) is None


def test_invalid_file_content(
    license_finder: LicenseFinder, root_directory_invalid: str
) -> None:
    invalid_files = [os.path.join(root_directory_invalid, "license.md")]
    all_license_info = license_finder.find_all_license_information(
        root_directory_invalid
    )
    for file_path in invalid_files:
        assert all_license_info.get(file_path) == LicenseType.UNKNOWN


@pytest.mark.asyncio
async def test_invalid_file_content_async(
    license_finder: LicenseFinder, root_directory_invalid: str
) -> None:
    invalid_files = [os.path.join(root_directory_invalid, "license.md")]
    all_license_info = await license_finder.find_all_license_information_async(
        root_directory_invalid
    )
    for file_path in invalid_files:
        assert all_license_info.get(file_path) == LicenseType.UNKNOWN


def test_setup_cfg_license(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    setup_cfg_path = os.path.join(root_directory_valid, "setup.cfg")
    all_license_info = license_finder.find_all_license_information(root_directory_valid)
    assert all_license_info.get(setup_cfg_path) == LicenseType.MIT


@pytest.mark.asyncio
async def test_setup_cfg_license_async(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    setup_cfg_path = os.path.join(root_directory_valid, "setup.cfg")
    all_license_info = await license_finder.find_all_license_information_async(
        root_directory_valid
    )
    assert all_license_info.get(setup_cfg_path) == LicenseType.MIT


def test_pyproject_toml_license(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    pyproject_toml_path = os.path.join(root_directory_valid, "pyproject.toml")
    all_license_info = license_finder.find_all_license_information(root_directory_valid)
    assert all_license_info.get(pyproject_toml_path) == LicenseType.MIT


@pytest.mark.asyncio
async def test_pyproject_toml_license_async(
    license_finder: LicenseFinder, root_directory_valid: str
) -> None:
    pyproject_toml_path = os.path.join(root_directory_valid, "pyproject.toml")
    all_license_info = await license_finder.find_all_license_information_async(
        root_directory_valid
    )
    assert all_license_info.get(pyproject_toml_path) == LicenseType.MIT
