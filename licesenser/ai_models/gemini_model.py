from langchain_google_vertexai import ChatVertexAI  # type: ignore

from licesenser.ai_models.ai_interface import AIModelInterface


class GeminiModel(AIModelInterface):
    """
    Gemini AI implementation of the AIModelInterface.
    Uses Gemini's API to recommend license types and generate license files.
    """

    def __init__(self: "GeminiModel", model: str = "gemini-1.5-pro") -> None:
        self.ai_model = ChatVertexAI(model_name=model, temperature=0, max_tokens=1000)

    async def recommend_license(self: "GeminiModel", project_info: dict) -> list:
        """
        Use Gemini API to recommend license types based on project information.
        :param project_info: dict containing project details.
        :return: list of recommended licenses
        """
        prompt = (
            "Based on the following project description, recommend a suitable open-source license:\n"
            f"{project_info}\n\n"
            "Provide a license name only."
        )
        license_recommendation = await self.ai_model(prompt)
        return license_recommendation.strip()

    async def generate_license_file(
        self: "GeminiModel", license_type: str, path: str
    ) -> None:
        """
        Generate a license file based on a selected license type.
        :param license_type: The selected license type.
        :param path: The path where the file will be saved.
        """
        prompt = f"Generate the content for this open-source license: {license_type}"
        license_content = await self.ai_model(prompt)
        return license_content.strip()
