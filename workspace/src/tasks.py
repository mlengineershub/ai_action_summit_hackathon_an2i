from typing import Any, Dict, List, Optional

from workspace.src.celery_app import celery
from workspace.src.detect_prescription_anomalies import detect_prescription_anomalies
from workspace.src.extract_ordonnance_data import (
    extract_ordonnance_data,
    summarize_ordonnances,
)
from workspace.src.gather_medical_knowledge_tool import (
    search_medical_articles,
    generate_search_summary,
)
from workspace.src.report_generation import generate_report
from workspace.src.utils import initialize_client, generate_prompt
from workspace.src.prompts import (
    detect_medical_prescription_anomaly_prompt_template,
    extract_ordonnance_data_prompt_template,
    summarize_ordonnances_prompt_template,
    report_generation_template,
    summarize_search_prompt_template,
)

client = initialize_client()


@celery.task(bind=True, name="workspace.src.tasks.detect_anomalies_task")
def detect_anomalies_task(
    self: Any, doctor_prescription: str, patient_medication_history: str
) -> Dict[str, Any]:
    """Celery task for detecting prescription anomalies."""
    prompt = generate_prompt(
        detect_medical_prescription_anomaly_prompt_template,
        doctor_prescription=doctor_prescription,
        patient_medication_history=patient_medication_history,
    )
    return detect_prescription_anomalies(client, prompt)


@celery.task(bind=True, name="workspace.src.tasks.extract_ordonnance_task")
def extract_ordonnance_task(self: Any, doctor_prescription: str) -> Dict[str, Any]:
    """Celery task for extracting ordonnance data."""
    prompt = generate_prompt(
        extract_ordonnance_data_prompt_template,
        doctor_prescription=doctor_prescription,
    )
    return {"extracted_data": extract_ordonnance_data(client, prompt)}


@celery.task(bind=True, name="workspace.src.tasks.summarize_ordonnances_task")
def summarize_ordonnances_task(
    self: Any, doctor_prescriptions: List[str]
) -> Dict[str, str]:
    """Celery task for summarizing multiple ordonnances."""
    prompt = generate_prompt(
        summarize_ordonnances_prompt_template,
        doctor_prescriptions=doctor_prescriptions,
    )
    return {"summary": summarize_ordonnances(client, prompt)}


@celery.task(bind=True, name="workspace.src.tasks.search_articles_task")
def search_articles_task(
    self: Any, query: str, retmax: Optional[int] = 5
) -> Dict[str, Any]:
    """Celery task for searching medical articles."""
    return {"results": search_medical_articles(query, retmax or 5)}


@celery.task(bind=True, name="workspace.src.tasks.generate_search_summary_task")
def generate_search_summary_task(
    self: Any, patient_condition: str, medical_articles: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Celery task for generating search summaries."""
    prompt = generate_prompt(
        summarize_search_prompt_template,
        patient_condition=patient_condition,
        medical_articles=medical_articles,
    )
    return generate_search_summary(client, prompt)


@celery.task(bind=True, name="workspace.src.tasks.generate_report_task")
def generate_report_task(
    self: Any,
    conversation: str,
    patient_information: Dict[str, Any],
    medical_history: str,
    additional_notes: str,
    additional_medical_information: str,
) -> Dict[str, Any]:
    """Celery task for generating medical reports."""
    prompt = generate_prompt(
        report_generation_template,
        conversation=conversation,
        patient_information=patient_information,
        medical_history=medical_history,
        additional_notes=additional_notes,
        additional_medical_information=additional_medical_information,
    )
    return generate_report(client, prompt)
