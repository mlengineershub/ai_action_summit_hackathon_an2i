from workspace.src.utils import (
    initialize_client,
    generate_prompt,
    generate_response,
)
from workspace.src.prompts import (
    extract_ordonnance_data_prompt_template,
    summarize_ordonnances_prompt_template,
    summarize_ordonnances_system_prompt,
)
from openai import OpenAI


def extract_ordonnance_data(client: OpenAI, prompt: str) -> str:
    system_prompt = extract_ordonnance_data_prompt_template
    response: str = generate_response(client, system_prompt, prompt)
    return response


def summarize_ordonnances(client: OpenAI, prompt: str) -> str:
    system_prompt = summarize_ordonnances_system_prompt
    response: str = generate_response(client, system_prompt, prompt)
    return response


# Example usage: ======================================== (will be removed)
client = initialize_client()

prescription1 = """Patient: John Doe
Date of Birth: 01/01/1970
Date of Consultation: 01/01/2022
Doctor: Dr. Jane Smith
Medication: Amoxicillin 500mg
Dosage: 1 capsule every 8 hours
Duration: 7 days
Refill: 0
Instructions: Take with food
"""

prescription2 = """Patient: Jane Doe
Date of Birth: 01/01/1980
Date of Consultation: 01/01/2022
Doctor: Dr. John Smith
Medication: Ibuprofen 200mg
Dosage: 1 tablet every 6 hours
Duration: 3 days
Refill: 1
Instructions: Take as needed for pain
"""

extraction_prompt1 = generate_prompt(
    extract_ordonnance_data_prompt_template,
    doctor_prescription=prescription1,
)

extraction_prompt2 = generate_prompt(
    extract_ordonnance_data_prompt_template,
    doctor_prescription=prescription2,
)

response1 = extract_ordonnance_data(client, extraction_prompt1)
response2 = extract_ordonnance_data(client, extraction_prompt2)

print(response1)
print(response2)

summary_prompt = generate_prompt(
    summarize_ordonnances_prompt_template, doctor_prescriptions=[response1, response2]
)

summary_response = summarize_ordonnances(client, summary_prompt)
print(summary_response)
