from workspace.src.utils import (
    generate_structured_response,
)
from workspace.src.prompts import detect_medical_prescription_anomaly_system_prompt
from openai import OpenAI
from workspace.src.pydantic_models import PrescriptionAnomalies
from typing import Any


def detect_prescription_anomalies(client: OpenAI, prompt: str) -> dict[str, Any]:
    system_prompt = detect_medical_prescription_anomaly_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, PrescriptionAnomalies
    )
    return response


# # Example usage: ======================================== (will be removed)
# client = initialize_client()
# # add a hsitorical data where a patient did not respect the prescription
# historical_prescription = """Patient: John Doe
# Date of Birth: 01/01/1970
# Date of Consultation: 01/01/2022
# Doctor: Dr. Jane Smith
# Medication: Amoxicillin 500mg
# Dosage: 1 capsule every 8 hours
# Duration: 7 days
# Refill: 0
# Instructions: Take with food
# """

# add a prescription that is not respected
prescription = """Patient: John Doe
Date of Birth: 01/01/1970
Date of Consultation: 01/01/2022
Doctor: Dr. Jane Smith
Medication: Amoxicillin 500mg

Dosage: 1 capsule every 8 hours
Duration: 7 days
Refill: 0
Instructions: Take with food
"""


# prompt = generate_prompt(
#     detect_medical_prescription_anomaly_prompt_template,
#     doctor_prescription=historical_prescription,
#     patient_medication_history=prescription,

# )

# response = detect_prescription_anomalies(client, prompt)
# print(response)
# ====================================================== (will be removed)
