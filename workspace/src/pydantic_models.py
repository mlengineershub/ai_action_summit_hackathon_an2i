from pydantic import BaseModel


class Patient(BaseModel):
    full_name: str
    age: str
    occupation: str
    sex: str
    chronical_diseases: list[str]
    allergies: list[str]


class ConsultationReport(BaseModel):
    symptoms: list[str]
    pathology: str
    treatment: list[str]
    keywords: list[str]
    summary: str


class SearchPropositions(BaseModel):
    search_propositions: list[str]


class SearchSummary(BaseModel):
    search_summary: str
    key_insights: list[str]


class FollowUpQuestions(BaseModel):
    follow_up_questions: list[str]


class PertinentMedicalPoints(BaseModel):
    pertinent_medical_points: list[str]

class PrescriptionAnomalies(BaseModel):
    prescription_anomalies: list[str]
