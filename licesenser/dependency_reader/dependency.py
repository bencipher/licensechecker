from abc import ABC, abstractmethod
from typing import Union


class DependencyReader(ABC):
    @abstractmethod
    def read_dependencies(
        self: "DependencyReader", file_path: str
    ) -> Union[set[str], dict[str, str]]:  # type: ignore
        pass
