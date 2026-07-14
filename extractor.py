from dotenv import load_dotenv
from openai import OpenAI
import os
import constants

load_dotenv()

LLM_Client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)  # Initialize the client with your API key

# LLM_Client.models.list_models()  # List available models

text = "Anthropic today introduced Claude Code Studio, a new AI-assisted development environment designed to help software engineers build, test, and deploy applications more efficiently. The platform integrates with GitHub, VS Code, and JetBrains IDEs, allowing developers to access Claude's reasoning capabilities directly inside their coding workflow. According to Anthropic, Claude Code Studio is powered by the Claude Opus 4 model and supports integration with the Model Context Protocol (MCP), enabling AI agents to securely interact with external tools and enterprise systems. The company stated that the platform can reduce debugging time by up to 35% while improving code quality.Anthropic also announced a strategic collaboration with Atlassian to bring AI-powered code review and documentation generation into software development teams. The integration will become available through Anthropic Enterprise later this year.During the announcement, Anthropic emphasized its commitment to responsible AI by introducing new security controls, including permission-based tool access, audit logging, and enterprise authentication."
def extractor(text) -> str:
    # text = file_path.read_text()
    response = LLM_Client.chat.completions.create(
        model="deepseek/deepseek-v4-flash",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Extract the text from the file and return it in a valid only JSON format . "
                    "Do NOT include:"
                    "- markdown"
                    "- explanations"
                    "- notes"
                    "- comments"
                    "- ```json"

                    "The response MUST start with {"

                    "The response MUST end with }"
                    f"Entities list should be in the format of name and type of entity, and relationships list should be in the format "
                    f"containing entity_name1, relationship_type entity_name2 as one relationship and add multiple relationships as you see, with confidence score and "
                    f"add an event list with event_name, type, subject, description, confidence_score and add multiple events as you see, with confidence score. "
                    f"Choose the closest type from this list {constants.ENTITY_TYPES},{constants.RELATIONSHIP_TYPES},{constants.EVENT_TYPES}. If none fits, use UNKNOWN. "
                    "\n\n"
                    f"File content:\n{text}"
                )
            }
        ]
    )

    return response.choices[0].message.content

# print(extractor(text))
