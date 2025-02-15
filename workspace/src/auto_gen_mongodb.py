from workspace.src.utils import (
    initialize_client,
    generate_prompt,
    generate_structured_response,
)
from workspace.src.prompts import (
    report_generation_template,
    report_generation_system_prompt,
)
from workspace.src.pydantic_models import ConsultationReport
from pymongo import MongoClient
from typing import Any, List

def get_mongo_client() -> MongoClient:
    return MongoClient("mongodb://localhost:27017/")

def initialize_db():
    client = get_mongo_client()
    db = client['hospital_db']
    consultations = db['Consultation']
    consultations.create_index("keywords")  # Ensure keywords are indexed
    return db

def aggregate_medical_history(summaries: List[str]) -> str:
    if not summaries:
        return "No previous consultations found."
    return " ".join(summaries)

def generate_report(client: Any, prompt: str) -> dict[str, Any]:
    system_prompt = report_generation_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, ConsultationReport
    )
    return response

def fetch_related_consultations(db, keywords: List[str]) -> List[str]:
    consultations = db['Consultation']
    related = consultations.find({"keywords": {"$in": keywords}}, {"summary": 1, "_id": 0})
    summaries = [consultation["summary"] for consultation in related]
    return summaries

def generate_and_insert_fake_data(patient_id: str, new_keywords: List[str]):

    db = initialize_db()
    client = initialize_client()

    # Fetch related consultations and aggregate medical history
    related_summaries = fetch_related_consultations(db, new_keywords)
    medical_history = aggregate_medical_history(related_summaries)

    # Mock values for new consultation
    patient_information = "Name: Jane Smith; Age: 32; Gender: Female; Patient ID: JS456; Contact: (987) 654-3210"
    report_date = "2025-02-15"
    doctor_name = "Dr. Emily Carter"
    facility_name = "City Hospital"
    conversation = """Patient: I've been having headaches for the past week. Doctor: Have you experienced nausea or sensitivity to light?
    Patient: Yes, both. Doctor: I'll recommend a CT scan and prescribe some medication."""

    # Format the template with updated medical history
    formatted_template = generate_prompt(
        prompt_template=report_generation_template,
        conversation=conversation,
        patient_information=patient_information,
        medical_history=medical_history,  # Recalculated medical history
    )

    # Generate the report using OpenAI
    new_report = generate_report(client, formatted_template)

    # Insert the new consultation into the database
    consultation_data = {
        "patient_id": patient_id,
        "symptoms": new_report["symptoms"],
        "pathology": new_report["pathology"],
        "treatment": new_report["treatment"],
        "keywords": new_keywords,
        "summary": new_report["summary"],
    }

    db['Consultation'].insert_one(consultation_data)
    print("New consultation inserted successfully.")
