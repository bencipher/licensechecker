from langchain_openai import OpenAI  # type: ignore

from licesenser.ai_models.gemini_model import AIModelInterface


class OpenAIModel(AIModelInterface):
    """
    OpenAI implementation of the AIModelInterface.
    Uses OpenAI API to recommend license types and generate license files.
    """

    def __init__(self: "OpenAIModel", api_key: str, model: str = "gpt-4") -> None:
        self.ai_model = OpenAI(
            model=model, temperature=0, max_tokens=500, api_key=api_key, max_retries=3
        )

    async def recommend_license(self: "OpenAIModel", project_info: dict) -> list:
        """
        Use OpenAI to recommend license types based on project information.
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
        self: "OpenAIModel", license_type: str, path: str
    ) -> None:
        """
        Generate a license file using OpenAI based on a selected license type.
        :param license_type: The selected license type.
        :param path: The path where the file will be saved.
        """
        prompt = f"Generate the content for this open-source license: {license_type}"
        license_content = await self.ai_model(prompt)
        return license_content.strip()
