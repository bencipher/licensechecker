from abc import ABC, abstractmethod


class DependencyReader(ABC):
    @abstractmethod
    def read_dependencies(self: "DependencyReader", file_path: str) -> set[str]:  # type: ignore
        pass
