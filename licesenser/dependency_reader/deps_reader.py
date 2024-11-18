from .dependency import DependencyReader


class DependencyFileReader:
    def __init__(self: "DependencyFileReader", strategy: DependencyReader) -> None:
        self._strategy = strategy

    def set_strategy(self: "DependencyFileReader", strategy: DependencyReader) -> None:
        self._strategy = strategy

    def list_dependencies(self: "DependencyFileReader", file_path: str) -> dict:
        return self._strategy.read_dependencies(file_path)
