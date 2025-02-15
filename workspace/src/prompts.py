report_generation_system_prompt = (
    "Generate a full medical report based on the following template."
)
report_generation_template = """ Your task is to generate a full medical report strictly following the provided template. You MUST NOT modify the format, structure, or section headers.  
- Every section must be filled exactly as specified, using only the placeholders provided.  
- If any information is missing, insert "Not Provided" instead of removing or modifying the structure.  
- You are NOT allowed to change, rewrite, or add extra explanations.  
- Do not summarize or interpret beyond what is provided. Just insert the correct details.  
- Ensure professional medical terminology and formatting consistency.  

---

#### Conversation between Doctor and Patient
{conversation}

---

#### Patient Information  
{patient_information}  

---

#### Medical History  
{medical_history}  

---

#### Additional Notes from the doctor
{additional_notes}  

---

#### Additional Medical Information
{additional_medical_information}

---
#### Generated Report
"""

search_proposition_system_prompt = "You are a very helpful Medical AI Assistant. You have been asked to provide medical search propositions based on the conversation between a doctor and a patient."

search_proposition_prompt_template = """Based on the current conversation between the doctor and the patient, provide relevant search propositions that could help the doctor in diagnosing the patient's condition. The search queries must be related to very niche medical topics that are related to the current conversation, and not general queires.
Do not provide previously searched information.
---
#### Conversation between Doctor and Patient
{conversation}
---
#### Previous Search History (Do not repeat these)
{search_history}
---
#### Search Propositions"""

summarize_search_system_prompt = "You are a Medical AI Assistant. You have been asked to provide a summary of many medical articles on a specific topic that a patient is suffering from. Your objective is to summarize the articles with a focus on the patient situation."

summarize_search_prompt_template = """Based on the medical articles provided, summarize the key points that are relevant to the patient's situation. The patient is suffering from a specific medical condition, and the doctor needs a concise summary of the articles to understand the condition better.
On the search_summary field summarize in few sentences the most relevant information from the articles.
On the key_insights field, provide the most important insights extracted from the from the articles that are related to the patient's condition.
Ensure that the summary and the key_insights are informative and contain medical jaragon.
---
#### Patient Medical Condition
{patient_condition}
---
#### Medical Articles
{medical_articles}
---
#### Summary"""

follow_up_questions_system_prompt = "You are a Medical AI Assistant. You have been asked to generate follow-up questions based on a conversation between a doctor and a patient."

follow_up_questions_prompt_template = """Based on the conversation between the doctor and the patient, generate follow-up questions that the doctor might ask to further understand the patient's condition. The questions should be relevant to the symptoms and medical history discussed in the conversation.
---
#### Conversation between Doctor and Patient
{conversation}
---
Follow-up Questions"""

extract_medical_points_system_prompt = "You are a Medical AI Assistant. You have been asked to extract pertinent medical points from a conversation between a doctor and a patient. A pertinent point is any information that is crucial and that the doctor should not forget or overlook."

extract_medical_points_prompt_template = """Extract the pertinent medical points from the conversation between the doctor and the patient. These points are crucial for the doctor to consider when diagnosing the patient's condition or planning the treatment.
---
#### Conversation between Doctor and Patient
{conversation}
---
#### Patient Previous Medical 
{previous_medical_history}
---
Pertinent Medical Points"""

extract_ordonnance_data_system_prompt = "You are a Medical AI Assistant. You have been asked to extract the medication data from a doctor's prescription."

extract_ordonnance_data_prompt_template = """Extract the medication data from the doctor's prescription. The prescription contains information about the medication, dosage, and frequency of use. The extracted data should be structured and organized for easy reference.
Summarize the medication data in a clear and concise paragraph.
---
#### Doctor's Prescription
{doctor_prescription}
---
Summerized Medication Data"""

summarize_ordonnances_system_prompt = "You are a Medical AI Assistant. You have been asked to summarize multiple doctor's prescriptions into a concise format."

summarize_ordonnances_prompt_template = """Summarize the medication data from multiple doctor's prescriptions into a concise format. The summary should include the medication names, dosages, and frequencies of use for each prescription.
---
#### Doctor's Prescriptions
{doctor_prescriptions}
---
Full Summarized Medication Data"""
