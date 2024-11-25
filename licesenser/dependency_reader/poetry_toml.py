import toml

from .dependency import DependencyReader


def parse_nested_poetry_deps(input: dict[str, str], output: set[str]) -> None:
    for k, v in input.items():
        if isinstance(v, dict):
            v = v.get("version", "*").strip("=")
        output.add(f"{k}={v}")


class PyprojectTomlReader(DependencyReader):
    def read_dependencies(self: "PyprojectTomlReader", file_path: str) -> set[str]:
        deps = set()
        print(deps)
        with open(file_path, "r") as file:
            pyproject = toml.load(file)

        parse_nested_poetry_deps(
            pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {}), deps
        )
        groups = pyproject.get("tool", {}).get("poetry", {}).get("group", {})
        for group in groups.values():
            parse_nested_poetry_deps(group.get("dependencies", {}), deps)
        return deps
