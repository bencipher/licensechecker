from __future__ import annotations

from importlib import metadata
from typing import Any, Optional

from requests.exceptions import ConnectTimeout

from licesenser.connections import session
from licesenser.schemas import JOINS, UNKNOWN, PackageInfo, ucstr


def get_license_from_classifier(classifiers: list[str] | None | list[Any]) -> ucstr:
    """Get license string from a list of project classifiers.

    Args:
    ----
            classifiers (list[str]): list of classifiers

    Returns:
    -------
            str: the license name

    """
    if not classifiers:
        return UNKNOWN
    licenses: list[str] = []
    for _val in classifiers:
        val = str(_val)
        if val.startswith("License"):
            lice = val.split(" :: ")[-1]
            if lice != "OSI Approved":
                licenses.append(lice)
    return ucstr(JOINS.join(licenses) if len(licenses) > 0 else UNKNOWN)


def create_package_info(
    name: Optional[str],
    local_version: Optional[str] = None,
    latest_version: Optional[str] = None,
    homepage: Optional[str] = None,
    author: Optional[str] = None,
    author_email: Optional[str] = None,
    size: int = -1,
    license: ucstr = ucstr("UNKNOWN"),
    error_code: int = 0,
) -> PackageInfo:
    """Create a PackageInfo instance with validation."""

    if name is None:
        raise ValueError("Package name cannot be None")

    return PackageInfo(
        name=name,
        local_version=local_version or ucstr("UNKNOWN"),
        latest_version=latest_version or ucstr("UNKNOWN"),
        homepage=homepage,
        author=author,
        author_email=author_email,
        size=size,
        license=license,
        error_code=error_code,
    )


def get_deps_info_from_local(requirement: ucstr) -> PackageInfo:
    """Get package info from local files including version, author
    and	the license.

    :param str requirement: name of the package
    :raises ModuleNotFoundError: if the package does not exist
    :return PackageInfo: package information
    """
    try:
        package_details = metadata.Distribution.from_name(requirement)
        pkg_meta = package_details.metadata
        lice = get_license_from_classifier(pkg_meta.get_all("Classifier"))
        if lice == UNKNOWN:
            lice = pkg_meta.get("License")
        name = pkg_meta.get("Name")
        version = pkg_meta.get("Version")
        homePage = pkg_meta.get("Home-page")
        author = pkg_meta.get("Maintainer") or pkg_meta.get("Author")
        author_email = pkg_meta.get("Maintainer-email")
        if not author_email:
            author_email = pkg_meta.get("Author-email")
            if author_email and "<" in author_email:
                author_email = author_email.split("<")[1][:-1]
                if not author:
                    author = author_email.split("<")[0][:-1]
        size = 0
        pkg_files = package_details.files
        if pkg_files is not None:
            size = sum(pp.size for pp in pkg_files if pp.size is not None)

        # Use the helper function to create PackageInfo
        return create_package_info(
            name=name,
            local_version=version,
            homepage=homePage,
            author=author,
            author_email=author_email,
            size=size,
            license=ucstr(lice),
        )

    except metadata.PackageNotFoundError as error:
        raise ModuleNotFoundError from error


def get_deps_info_from_pypi(requirement: ucstr) -> PackageInfo:
    """Get package info from PyPI."""
    try:
        request = session.get(f"https://pypi.org/pypi/{requirement}/json", timeout=3)
        response = request.json()
        info = response.get("info", {})
        licenseClassifier = get_license_from_classifier(info["classifiers"])

        size = -1
        urls = response.get("urls", [])
        if urls:
            size = int(urls[-1]["size"])
        author_email = info.get("Maintainer-email")
        if not author_email:
            author_email = (
                info.get("author_email")
                or info.get("Author-email")
                or info.get("Author_email")
            )
            if author_email and "<" in author_email:
                author_email = author_email.split("<")[1][:-1]

        # Use the helper function to create PackageInfo
        return create_package_info(
            name=info.get("name"),
            latest_version=info.get("version"),
            homepage=info.get("home_page"),
            author=info.get("author"),
            author_email=author_email,
            size=size,
            license=ucstr(
                licenseClassifier
                if licenseClassifier != UNKNOWN
                else info.get("license", UNKNOWN) or UNKNOWN
            ),
        )
    except ConnectTimeout as error:
        print("error here after timeout")
        raise ModuleNotFoundError from error
    except KeyError as error:
        raise ModuleNotFoundError from error


def get_project_packages(reqs: set[str]) -> set[PackageInfo]:
    """Get dependency info"""
    packageinfo = set()
    for deps in reqs:
        requirement = ucstr(deps.split("=")[0])
        if requirement == "python":
            continue
        try:
            packageinfo.add(get_deps_info_from_local(requirement))
        except ModuleNotFoundError:
            try:
                packageinfo.add(get_deps_info_from_pypi(requirement))
            except ModuleNotFoundError:
                print("Could not get info", requirement)
                packageinfo.add(create_package_info(name=requirement, error_code=1))

    return packageinfo
