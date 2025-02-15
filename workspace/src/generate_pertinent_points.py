from workspace.src.utils import (
    generate_structured_response,
)
from workspace.src.prompts import (
    extract_medical_points_system_prompt,
)
from openai import OpenAI
from workspace.src.pydantic_models import PertinentMedicalPoints
from typing import Any


def extract_pertinent_medical_points(client: OpenAI, prompt: str) -> dict[str, Any]:
    system_prompt = extract_medical_points_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, PertinentMedicalPoints
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

# previous_medical_patient_report = """Patient has no known history of heart conditions or high blood pressure. Patient has been experiencing chest pain since last night with no other symptoms. Doctor recommends running tests to check heart function and blood pressure.
# Patient is not suffering of any cancer or other terminal diseases. Patient has a history of allergies to penicillin and sulfa drugs. Patient has a history of asthma and has been using an inhaler for the past 5 years.
# Patient has a history of high blood pressure and has been taking medication for the past 2 years. Patient has a history of heart disease and has undergone a bypass surgery 10 years ago."""

# prompt = generate_prompt(
#     extract_medical_points_prompt_template,
#     conversation=conversation,
#     previous_medical_history=previous_medical_patient_report,
# )

# response = extract_pertinent_medical_points(client, prompt)
# print(response)
# # ====================================================== (will be removed)
