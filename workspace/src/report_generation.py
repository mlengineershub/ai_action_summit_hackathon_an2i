from workspace.src.utils import (
    initialize_client,
    generate_prompt,
    generate_structured_response,
)
from workspace.src.prompts import (
    report_generation_template,
    report_generation_system_prompt,
)
from openai import OpenAI
from workspace.src.pydantic_models import ConsultationReport
from typing import Any


def generate_report(client: OpenAI, prompt: str) -> dict[str, Any]:
    system_prompt = report_generation_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, ConsultationReport
    )
    return response


# =======================================================
if __name__ == "__main__":
    # Example usage: ========================================
    client = initialize_client()

    template = """
    Medical Report Template
    -----------------------
    - Report Date: {report_date}
    - Doctor: {doctor_name}
    - Facility: {facility_name}

    Sections:
    1. Patient Information: Detailed patient demographics.
    2. Medical History: Summary of past medical conditions, surgeries, medications, and allergies.
    3. Examination and Findings: Documentation of vital signs and physical examination results.
    4. Diagnosis and Treatment Plan: Physician's diagnosis, differential diagnosis, and recommended treatments.
    5. Additional Notes: Further observations or recommendations from the attending doctor.
    6. Additional Medical Information: Relevant lab results, imaging studies, or other diagnostics.
    """
    # flake8: noqa

    # Concise mock values for testing
    patient_information = "Name: John Doe; Age: 45; Gender: Male; Social Security Number: 1009634576; Contact: (123) 456-7890"
    medical_history = "Hypertension; Diabetes; Previous Surgery: Appendectomy; Medications: Metformin, Lisinopril; Allergies: None"
    anomaly_detection = (
        "No anomalies detected in the patient's medical history or examination."
    )

    # Optionally, you could also define additional variables for the realistic template if needed:
    report_date = "2025-02-15"
    doctor_name = "Dr. Emily Carter"
    facility_name = "City Hospital"
    conversation = """Patient: I have been experiencing chest pain. Doctor: When did the pain start?
    Patient: It started last night and has been persistent since then.
    Doctor: Have you experienced any shortness of breath or dizziness with the pain?
    Patient: No, I haven't experienced any other symptoms with the chest pain.
    Doctor: I will conduct a physical examination to assess the situation further."""

    # Format the realistic template with its own variables
    formatted_template = generate_prompt(
        prompt_template=report_generation_template,
        conversation=conversation,
        patient_information=patient_information,
        medical_history=medical_history,
        anomaly_detection=anomaly_detection,
    )

    response = generate_report(client, formatted_template)
    print("Response:", response)

# =======================================================
