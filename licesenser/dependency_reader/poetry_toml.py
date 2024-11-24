import toml

from .dependency import DependencyReader


class PyprojectTomlReader(DependencyReader):
    def read_dependencies(self: "PyprojectTomlReader", file_path: str) -> set[str]:
        deps = set()
        with open(file_path, "r") as file:
            pyproject = toml.load(file)

        # Extract main dependencies
        main_deps = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
        deps.update(f"{k}={v}" for k, v in main_deps.items())

        # Extract group dependencies
        groups = pyproject.get("tool", {}).get("poetry", {}).get("group", {})
        for group_deps in groups.values():
            deps.update(
                f"{k}={v}" for k, v in group_deps.get("dependencies", {}).items()
            )

        return deps
