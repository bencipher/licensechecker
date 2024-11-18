import toml  # type: ignore

from .dependency import DependencyReader


class PyprojectTomlReader(DependencyReader):
    def read_dependencies(self: "PyprojectTomlReader", file_path: str) -> dict:
        with open(file_path, "r") as file:
            pyproject = toml.load(file)
        return pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
