from workspace.src.utils import (
    initialize_client,
    generate_prompt,
    generate_structured_response,
    generate_response,
)
from workspace.src.prompts import (
    report_generation_template,
    report_generation_system_prompt,
    system_prompt_synthese,
    prompt_template_synthese,
)
from workspace.src.pydantic_models import ConsultationReport
from pymongo import MongoClient
from typing import Any, List, Tuple
from openai import OpenAIDict
import urllib.parse
from dotenv import load_dotenv
import os
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional, Any, Dict, List

load_dotenv()
USERNAME_MONGODB: str = os.getenv("USERNAME_MONGODB", "")
PASSWORD_MONGODB: str = os.getenv("PASSWORD_MONGODB", "")
INSTANCE_MONGODB: str = os.getenv("INSTANCE_MONGODB", "")
REGION_MONGODB: str = os.getenv("REGION_MONGODB", "")
PATH_TLS_CERTIFICATE_MONGODB: str = os.getenv("PATH_TLS_CERTIFICATE_MONGODB", "")

CLIENT = initialize_client()



def get_mongo_client() -> MongoClient:
    username = urllib.parse.quote_plus(USERNAME_MONGODB)
    password = urllib.parse.quote_plus(PASSWORD_MONGODB)  # URL-encode the colon
    instance_id = INSTANCE_MONGODB
    region = REGION_MONGODB  # the region of your database instance. "fr-par" if Paris
    tls_certificate = PATH_TLS_CERTIFICATE_MONGODB  # path to your TLS certificate file
    # Construct the connection string
    connection_string = (
        f"mongodb+srv://{username}:{password}@{instance_id}.mgdb.{region}.scw.cloud/"
        f"?tls=true&tlsCAFile={tls_certificate}"
    )
    client = MongoClient(connection_string)

    return client
    # flake8: noqa

def get_database(client: MongoClient)-> Database:
    client = get_mongo_client()
    db = client[USERNAME_MONGODB]
    return db

def get_table(db: Database,table_name: str) -> Collection:
    return db[table_name]

def create_index(table : Collection, fields: List[str]) -> None:
    table.create_index(fields)

def insert(table : Collection, document : Dict[str, Any] ) -> None:
    table.insert_one(document)

def find_one(table: Collection, query : Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return table.find_one(query)

def find(table: Collection, query : Dict[str, Any]) -> List[Dict[str, Any]]:
    return table.find(query)




def aggregate_medical_history(summaries: str) -> str:
    """
    Function that generates a medical record based on the provided summaries.

    Parameters:
        summaries (List[str]): A list of medical summaries from previous consultations.
        client (OpenAI): The OpenAI client instance.

    Returns:
        str: The generated medical record.
    """

    formatted_prompt = generate_prompt(
        prompt_template=prompt_template_synthese, summaries=summaries
    )
    response = generate_response(
        client=CLIENT,
        system_prompt=system_prompt_synthese,
        user_prompt=formatted_prompt,
    )
    return response


def generate_report(client: OpenAI, prompt: str) -> dict[str, Any]:
    system_prompt = report_generation_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, ConsultationReport
    )
    return response


def fetch_related_consultations(db: Database, ssn: str) -> Tuple[List[str], int]:
    consultations = get_table(db, table_name="Consultation")
    # get all consultations with the same patient ID
    ssn_query = {"social_security_number": ssn}
    related = find(consultations,ssn_query)
    summaries = [consultation["intelligent_summary"] for consultation in related]
    last_reportID = max([consultation["reportID"] for consultation in related])
    return summaries, last_reportID


def generate_and_insert_fake_data(
    ssn: str, report_date: str, conversation: str, patient_information: str
) -> None:
    
    # Initialize MongoDB
    db = get_database()

    # Fetch related consultations and aggregate medical history
    related_summaries, last_reported_id = fetch_related_consultations(db, ssn)
    formatted_summaries = ", ".join(related_summaries)
    medical_history = aggregate_medical_history(formatted_summaries)

    # Format the template with updated medical history
    formatted_template = generate_prompt(
        prompt_template=report_generation_template,
        conversation=conversation,
        patient_information=patient_information,
        medical_history=medical_history,
        anomaly_detection="Not Provided",
    )

    # Generate the report using OpenAI
    new_report = generate_report(CLIENT, formatted_template)

    reportId = int(last_reported_id) + 1

    # Insert the new consultation into the database
    consultation_data = {
        "reportID": reportId,
        "social_security_number": ssn,
        "symptoms": new_report["symptoms"],
        "pathology": new_report["pathology"],
        "treatment": new_report["treatment"],
        "keywords": new_report["keywords"],
        "date": report_date,
        "intelligent_summary": new_report["intelligent_summary"],
    }

    insert(db["Consultation"],consultation_data)
    print("New consultation inserted successfully.")


def add_new_patient(
    ssn: str,
    full_name: str,
    age: str,
    sex: str,
    occupation: str,
    chronical_diseases: List[str],
    allergies: List[str],
) -> bool:
    # Initialize MongoDB
    db = initialize_db()

    # Check whether the patient already exists
    patient = db["Patient"].find_one({"social_security_number": ssn})
    if patient:
        print("Patient already exists in the database.")
        return False

    # Insert the new patient into the database
    patient_data = {
        "social_security_number": ssn,
        "full_name": full_name,
        "age": age,
        "sex": sex,
        "occupation": occupation,
        "chronical_diseases": chronical_diseases,
        "allergies": allergies,
    }

    db["Patient"].insert_one(patient_data)
    print("New patient added successfully.")

    return True


if __name__ == "__main__":
    # Mock values for new consultation for a known patient identified by its SSN
    # # Note :
    # # # 1. We anonymized the name of the patient
    # # # 2. The Social security number is hashed so that it can't be used to identify the patient
    # # # 3. The conversation is a mock conversation between a doctor and a patient
    report_date = "2025-02-15"
    ssn = "123-45-6789"
    # Mock values for new consultation
    patient_information = f"age: 35; sex: Male; Social Security Number: {ssn}"
    list_conv = [
        """Patient: I've been feeling a sharp pain in my lower back. Doctor: Does the pain get worse with movement or when sitting? Patient: It's worse when I try to bend or lift something. Doctor: Have you experienced any numbness or tingling in your legs? Patient: Sometimes, especially when the pain is severe. Doctor: It could be a muscle strain or a slipped disc. I'll recommend an MRI and some pain relief medication in the meantime.""",
        """Patient: I've been having difficulty sleeping for the past month. Doctor: Do you find it hard to fall asleep, or do you wake up frequently? Patient: Both, I lie awake for hours, and then I wake up feeling tired. Doctor: Have you been under any stress or experiencing anxiety? Patient: Yes, my work has been overwhelming lately. Doctor: I'll recommend some relaxation techniques and prescribe a mild sleep aid. Let's monitor how you feel in a few weeks.""",
        """Patient: I've been having frequent nosebleeds. Doctor: How often do they occur, and how long do they last? Patient: About twice a day, and they last for a few minutes. Doctor: Have you been exposed to dry air or used any nasal sprays recently? Patient: Yes, I've been using a decongestant spray for my allergies. Doctor: Overuse of nasal sprays can cause nosebleeds. I'll suggest stopping the spray and using a saline solution instead.""",
        """Patient: I've been experiencing numbness in my hands. Doctor: Does it happen in both hands or just one? Patient: Both hands, and it’s worse at night. Doctor: Have you been using your hands for repetitive tasks like typing? Patient: Yes, I work on a computer all day. Doctor: It sounds like carpal tunnel syndrome. I'll recommend a wrist brace and some exercises to alleviate the symptoms.""",
        """Patient: I've been coughing a lot, and my chest feels tight. Doctor: Have you been exposed to any allergens or irritants recently? Patient: I recently started painting my house, and I noticed the cough started then. Doctor: It could be a reaction to the fumes. Have you experienced any fever or shortness of breath? Patient: No fever, but sometimes I feel a bit breathless. Doctor: I'll recommend taking a break from exposure and prescribe an inhaler if needed.""",
        """Patient: I've been feeling lightheaded and dizzy throughout the day. Doctor: Have you been eating regularly and staying hydrated? Patient: I sometimes skip meals, and I forget to drink water. Doctor: Have you experienced any fainting or blurred vision? Patient: No, just the dizziness. Doctor: It could be low blood sugar or dehydration. I'll recommend blood tests and suggest keeping a regular meal schedule.""",
        """Patient: I've been having trouble hearing in my right ear. Doctor: Did this happen suddenly, or has it been gradual? Patient: It started gradually a few weeks ago. Doctor: Have you had any ear pain, discharge, or ringing in the ear? Patient: Yes, there's a constant ringing sound. Doctor: It could be an earwax blockage or an infection. I'll examine your ear and possibly refer you to an ENT specialist.""",
        """Patient: I've been having a burning sensation when I urinate. Doctor: Have you noticed any blood in your urine or changes in its color? Patient: No blood, but it’s darker than usual. Doctor: How long has this been happening? Patient: About a week now. Doctor: It could be a urinary tract infection. I'll recommend a urine test and start you on antibiotics while we wait for the results.""",
        """Patient: I've been having a lot of headaches and blurry vision. Doctor: Do the headaches occur at specific times, like after reading or using the computer? Patient: Yes, they get worse in the evening. Doctor: Have you had your eyes checked recently? Patient: No, it’s been years. Doctor: It could be eye strain or a vision problem. I'll refer you to an optometrist for a check-up.""",
        """Patient: I've been feeling extremely fatigued and out of breath lately. Doctor: Have you been engaging in any strenuous physical activity? Patient: No, just my normal routine. Doctor: Have you noticed any swelling in your legs or any chest discomfort? Patient: Yes, my ankles have been swollen. Doctor: I'll recommend some blood tests and a cardiac evaluation to rule out any underlying conditions.""",
    ]
    for conversation in list_conv:
        generate_and_insert_fake_data(
            ssn, report_date, conversation, patient_information
        )

    # Mock add a new patient
    # 'social_security_number': '123-45-6789', 'full_name': 'John Doe', 'age': '35', 'sex': 'Male', 'occupation': 'Software Engineer', 'chronical_diseases': ['Diabetes'], 'allergies': ['Peanuts', 'Dust']}
    ssn = "987-65-4321"
    full_name = "Alice Smith"
    age = "45"
    sex = "Female"
    occupation = "Teacher"
    chronical_diseases = ["Hypertension"]
    allergies = ["Penicillin"]
    add_new_patient(ssn, full_name, age, sex, occupation, chronical_diseases, allergies)
