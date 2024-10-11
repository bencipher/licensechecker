from abc import ABC, abstractmethod


class AIModelInterface(ABC):
    """
    Interface for AI models to generate and recommend license types.
    Ensures that all AI implementations follow a common structure.
    """

    @abstractmethod
    async def recommend_license(self: "AIModelInterface", project_info: dict) -> list:
        """
        Method to recommend a list of possible license types based on project info.
        :param project_info: dict containing project details (dependencies, domain, etc.)
        :return: list of recommended license types
        """
        pass

    @abstractmethod
    async def generate_license_file(
        self: "AIModelInterface", license_type: str, path: str
    ) -> None:
        """
        Method to generate a license file of the specified type at the given path.
        :param license_type: The selected license type (e.g., MIT, Apache 2.0)
        :param path: The file path where the license will be created.
        """
        pass
