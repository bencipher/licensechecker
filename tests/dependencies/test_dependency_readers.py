from licesenser.dependency_reader.deps_reader import DependencyFileReader
from licesenser.dependency_reader.pipfile import PipfileReader
from licesenser.dependency_reader.poetry_toml import PyprojectTomlReader
from licesenser.dependency_reader.requirements_txt import RequirementsTxtReader


def test_pipfile_reader(pipfile_data: str) -> None:
    with open(pipfile_data, "r") as file:
        reader = PipfileReader()
        dependencies = reader.read_dependencies(file.name)

        expected_dependencies = {
            "requests": "*",
            "numpy": "==1.21.0",
            "pandas": {"version": "*", "markers": "python_version >= '3.6'"},
            "scipy": {"version": "==1.7.1", "markers": "python_version >= '3.6'"},
        }
        # assert file ends with Pipfile"
        assert dependencies == expected_dependencies


def test_pyproject_toml_reader(pyproject_data: str) -> None:
    with open(pyproject_data, "r") as file:
        reader = PyprojectTomlReader()
        dependencies = reader.read_dependencies(file.name)

        expected_dependencies = {
            "python": "^3.8",
            "requests": "^2.25.1",
            "numpy": "1.21.0",
            "pandas": "*",
            "scipy": {"version": "==1.7.1", "markers": "python_version >= '3.6'"},
        }
        # assert file ends with pyproject.toml"
        assert dependencies == expected_dependencies


def test_requirements_txt_reader(requirements_data: str) -> None:
    with open(requirements_data, "r") as file:
        reader = RequirementsTxtReader()
        dependencies = reader.read_dependencies(file.name)

        expected_dependencies = {
            "requests": "2.25.1",
            "numpy": "1.21.0",
            "pandas": "1.3.3",
            "scipy": "1.7.1",
        }
        # assert file ends with requirements.txt"
        assert dependencies == expected_dependencies


def test_dependency_context(
    pipfile_data: str, requirements_data: str, pyproject_data: str
) -> None:
    # Create instances of dependency readers
    pipfile_reader = PipfileReader()
    requirements_reader = RequirementsTxtReader()
    pyproject_reader = PyprojectTomlReader()

    # Create an instance of DependencyFileReader with different strategies
    dependency_file_reader = DependencyFileReader(pipfile_reader)

    # Test with Pipfile strategy
    assert isinstance(
        dependency_file_reader.list_dependencies(pipfile_data), dict
    ), "PipfileReader should return a dictionary"

    # Change strategy to Requirements.txt
    dependency_file_reader.set_strategy(requirements_reader)
    assert isinstance(
        dependency_file_reader.list_dependencies(requirements_data), dict
    ), "RequirementsTxtReader should return a dictionary"

    # Change strategy to pyproject.toml
    dependency_file_reader.set_strategy(pyproject_reader)
    assert isinstance(
        dependency_file_reader.list_dependencies(pyproject_data), dict
    ), "PyprojectTomlReader should return a dictionary"


def test_unsupported_file_type(unsupported_data: str) -> None:
    file_extension = unsupported_data.split(".")[-1]
    supported_extensions = ["Pipfile", "pyproject.toml", "requirements.txt"]
    assert (
        file_extension not in supported_extensions
    ), f"File extension {file_extension} is supported, expected unsupported type"
