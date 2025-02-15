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
