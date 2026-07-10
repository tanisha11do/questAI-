from dotenv import load_dotenv
from google import genai
import os
import constants

load_dotenv()

LLM_Client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

text = "NVIDIA today announced Dynamo, a new AI inference platform designed to optimize large language model deployment across GPU clusters. Dynamo integrates seamlessly with TensorRT-LLM and NVIDIA Triton Inference Server, enabling faster inference and better resource utilization for enterprise AI workloads.The platform supports popular open-source frameworks including vLLM and PyTorch, making it easier for developers to deploy production-ready AI applications.According to NVIDIA, Dynamo can improve inference throughput by up to 30% compared to previous deployment pipelines.The announcement also highlighted collaborations with Hugging Face, allowing developers to integrate Dynamo into existing machine learning workflows with minimal configuration. NVIDIA stated that Dynamo will be available through NVIDIA AI Enterprise later this year."

def extractor(text) -> str:
    # text = file_path.read_text()
    response = LLM_Client.models.generate_content(
        model="gemini-2.5-flash",
        contents=(
            f"Extract the text from the file and return it in a valid only JSON format no explanations, markdowns or codes. "
            f"Entities list should be in the format of name and type of entity, and relationships list should be in the format"
            f"containing entity_name1, relationship_type entity_name2 as one relationship and add multiple relationships as you see, with confidence score and"
            f"add an event listwith event_namme, type, subject, description, confidence score and add multiple events as you see, with confidence score. Choose the closest type from this list {constants.ENTITY_TYPES},{constants.RELATIONSHIP_TYPES},{constants.EVENT_TYPES},. If none fits, use UNKNOWN "
            "\n\n"
            f"File content:\n{text}"
        )
    )

    return response.text


