from .dependency import DependencyReader


class RequirementsTxtReader(DependencyReader):
    def read_dependencies(self: "RequirementsTxtReader", file_path: str) -> set[str]:
        """Read dependencies from a requirements.txt file and return them as a set of strings.

        Args:
            file_path (str): The path to the requirements.txt file.

        Returns:
            set[str]: A set of dependencies in the format 'package_name=version'.
        """
        dependencies = set()
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "==" in line:
                        package, version = line.split("==", 1)
                    else:
                        package, version = line, "*"
                    dependencies.add(f"{package.strip()}={version.strip()}")

        return dependencies
