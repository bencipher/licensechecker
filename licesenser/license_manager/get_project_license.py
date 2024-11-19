import asyncio
import logging
import os
import re
from typing import Union

import aiofiles  # type: ignore
import toml  # type: ignore

from licesenser.enums import LicenseType

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Define the files and directories to look for and exclude
target_files = [
    "license.md",
    "license.rst",
    "license.txt",
    "license",
    "setup.cfg",
    "pyproject.toml",
]
exclude_directories = [
    "environment",
    "tests",
    "alembic",
    ".git",
    ".env",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".vscode",
    "coverage",
]


def should_exclude(directory: str) -> bool:
    """Check if the given directory should be excluded."""
    return any(exclude_dir in directory for exclude_dir in exclude_directories)


class FileFinder:
    def find_files(self: "FileFinder", root_dir: str) -> list[str]:
        """Recursively find target files in the given root directory."""
        found_files = []
        for root, dirs, files in os.walk(root_dir):
            # Exclude directories
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
            # Find target files
            for file in files:
                if file.lower() in target_files:
                    found_files.append(os.path.join(root, file))
        return found_files


async def read_file_async(file_path: str) -> str:
    """Read the content of a file asynchronously."""
    async with aiofiles.open(file_path, "r") as f:
        return await f.read()


def identify_license_from_text(text: str) -> LicenseType:
    """Identify the license from the given text."""
    for license_type in LicenseType:
        if re.search(license_type.value, text, re.IGNORECASE):
            return license_type
    return LicenseType.UNKNOWN


async def identify_license_from_license_file(file_path: str) -> LicenseType:
    """Identify the license from a LICENSE file."""
    content = await read_file_async(file_path)
    return identify_license_from_text(content)


async def identify_license_from_pyproject_toml(
    file_path: str,
) -> LicenseType:
    """Identify the license from a pyproject.toml file."""
    content = await read_file_async(file_path)
    pyproject = toml.loads(content)
    license_info = pyproject.get("tool", {}).get("poetry", {}).get("license")
    if license_info:
        return identify_license_from_text(license_info)
    return LicenseType.NONE


async def identify_license_from_setup_cfg(file_path: str) -> LicenseType:
    """Identify the license from a setup.cfg file."""
    content = await read_file_async(file_path)
    lines = content.split("\n")
    license_info = None
    for line in lines:
        if line.startswith("license = "):
            license_info = line.split("=")[1].strip()
            break
    return (
        identify_license_from_text(license_info) if license_info else LicenseType.NONE
    )


async def extract_license_info_async(file_path: str) -> LicenseType:
    """Extract license information from the given file asynchronously."""
    file_name = os.path.basename(file_path)
    print(f"Checking {file_name=}")
    try:
        if file_name.upper() == "LICENSE" or re.match(
            r"^LICENSE\..*", file_name.upper()
        ):
            return await identify_license_from_license_file(file_path)
        elif file_name == "pyproject.toml":
            return await identify_license_from_pyproject_toml(file_path)
        elif file_name == "setup.cfg":
            return await identify_license_from_setup_cfg(file_path)
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
    return LicenseType.NONE


class LicenseFinder:
    def __init__(self: "LicenseFinder", file_finder: FileFinder) -> None:
        self.file_finder = file_finder
        self.license_extractor = extract_license_info_async

    def find_all_license_information(
        self: "LicenseFinder", root_dir: str
    ) -> Union[dict[str, LicenseType], None]:
        """Find and extract all license information from target files."""
        found_files = self.file_finder.find_files(root_dir)
        license_info = {}
        for file_path in found_files:
            print(f"{file_path=}")
            info = asyncio.run(self.license_extractor(file_path))
            if info:
                license_info[file_path] = info
        return license_info

    def find_first_license_information(
        self: "LicenseFinder", root_dir: str
    ) -> LicenseType:
        """Find and extract the first available license information from target files."""
        found_files = self.file_finder.find_files(root_dir)
        for file_path in found_files:
            info = asyncio.run(self.license_extractor(file_path))
            if info:
                return info
        return LicenseType.NONE

    async def find_all_license_information_async(
        self: "LicenseFinder", root_dir: str
    ) -> dict[str, LicenseType]:
        """Find and extract all license information from target files asynchronously."""
        found_files = self.file_finder.find_files(root_dir)
        tasks = [self.license_extractor(file_path) for file_path in found_files]

        results = await asyncio.gather(*tasks)
        license_info = {}
        for file_path, info in zip(found_files, results):
            if not info or isinstance(info, Exception):
                logging.error(f"Error processing {file_path}: {info}")
                continue
            license_info[file_path] = info
        return license_info

    async def find_first_license_information_async(
        self: "LicenseFinder", root_dir: str
    ) -> LicenseType:
        """Find and extract the first available license information from target files asynchronously."""
        found_files = self.file_finder.find_files(root_dir)
        for file_path in found_files:
            info = await self.license_extractor(file_path)
            if info:
                return info
        return LicenseType.NONE
