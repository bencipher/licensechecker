from .dependency import DependencyReader


class RequirementsTxtReader(DependencyReader):
    def read_dependencies(self: "RequirementsTxtReader", file_path: str) -> dict:
        dependencies = {}
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    package, version = (
                        line.split("==") if "==" in line else (line, None)
                    )
                    dependencies[package] = version
        return dependencies
