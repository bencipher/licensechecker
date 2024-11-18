from abc import ABC, abstractmethod


class DependencyReader(ABC):
    @abstractmethod
    def read_dependencies(self: "DependencyReader", file_path: str) -> dict:  # type: ignore
        pass
