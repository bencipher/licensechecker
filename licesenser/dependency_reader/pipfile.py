import toml

from .dependency import DependencyReader


class PipfileReader(DependencyReader):
    def read_dependencies(self: "PipfileReader", file_path: str) -> set[str]:
        """Read dependencies from a Pipfile and return them as a set of strings.

        Args:
            file_path (str): The path to the Pipfile.

        Returns:
            set[str]: A set of dependencies in the format 'package_name=version'.
        """
        dependencies = set()
        with open(file_path, "r") as file:
            pipfile = toml.load(file)

        package_sections = ["packages", "dev-packages"]
        for section in package_sections:
            for package_name, version in pipfile.get(section, {}).items():
                version = str(version).strip("=")
                dependencies.add(f"{package_name}={version}")
        return dependencies
