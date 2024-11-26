import toml

from licesenser.dependency_reader.utils import parse_nested_deps

from .dependency import DependencyReader


class PyprojectTomlReader(DependencyReader):
    def read_dependencies(self: "PyprojectTomlReader", file_path: str) -> set[str]:
        deps = set()
        try:
            if not file_path.endswith(".toml"):
                raise Exception("Only Toml Files allowed")

            with open(file_path, "r") as file:
                pyproject = toml.load(file)

            parse_nested_deps(
                pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {}),
                deps,
            )
            groups = pyproject.get("tool", {}).get("poetry", {}).get("group", {})
            for group in groups.values():
                parse_nested_deps(group.get("dependencies", {}), deps)
            return deps
        except FileNotFoundError as err:
            raise FileNotFoundError from err
