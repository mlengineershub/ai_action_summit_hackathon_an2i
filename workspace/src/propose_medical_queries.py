from workspace.src.utils import (
    initialize_client,
    generate_prompt,
    generate_structured_response,
)
from workspace.src.prompts import (
    search_proposition_prompt_template,
    search_proposition_system_prompt,
)
from openai import OpenAI
from workspace.src.pydantic_models import SearchPropositions
from typing import Any


def generate_search_propositions(client: OpenAI, prompt: str) -> dict[str, Any]:
    system_prompt = search_proposition_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, SearchPropositions
    )
    return response


# Example usage: ======================================== (will be removed)
client = initialize_client()

conversation = """Patient: I have been experiencing chest pain. Doctor: When did the pain start?
Patient: It started last night and has been persistent since then.
Doctor: Have you experienced any shortness of breath or dizziness with the pain?
Patient: No, I haven't experienced any other symptoms with the chest pain.
Doctor: Do you have any history of heart conditions or high blood pressure?
Patient: No, I don't have any known heart conditions or high blood pressure.
Doctor: I recommend running some tests to check your heart function and blood pressure."""
search_history = "Chest pain causes; Heart conditions; High blood pressure symptoms"

prompt = generate_prompt(
    search_proposition_prompt_template,
    conversation=conversation,
    search_history=search_history,
)

response = generate_search_propositions(client, prompt)
print(response)
# ====================================================== (will be removed)
