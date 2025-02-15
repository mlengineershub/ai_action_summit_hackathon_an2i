from workspace.src.utils import (
    generate_structured_response,
)
from workspace.src.prompts import (
    follow_up_questions_system_prompt,
)
from openai import OpenAI
from workspace.src.pydantic_models import FollowUpQuestions
from typing import Any


def generate_follow_up_questions(client: OpenAI, prompt: str) -> dict[str, Any]:
    system_prompt = follow_up_questions_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, FollowUpQuestions
    )
    return response


# # Example usage: ======================================== (will be removed)
# client = initialize_client()

# conversation = """Patient: I have been experiencing chest pain. Doctor: When did the pain start?
# Patient: It started last night and has been persistent since then.
# Doctor: Have you experienced any shortness of breath or dizziness with the pain?
# Patient: No, I haven't experienced any other symptoms with the chest pain.
# Doctor: Do you have any history of heart conditions or high blood pressure?
# Patient: No, I don't have any known heart conditions or high blood pressure.
# Doctor: I recommend running some tests to check your heart function and blood pressure."""


# prompt = generate_prompt(
#     follow_up_questions_prompt_template,
#     conversation=conversation,
# )

# response = generate_follow_up_questions(client, prompt)
# print(response)
# # ====================================================== (will be removed)
