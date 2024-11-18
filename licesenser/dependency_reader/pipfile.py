import toml  # type: ignore

from .dependency import DependencyReader


class PipfileReader(DependencyReader):
    def read_dependencies(self: "PipfileReader", file_path: str) -> dict:
        with open(file_path, "r") as file:
            pipfile = toml.load(file)
        return pipfile.get("packages", {})
