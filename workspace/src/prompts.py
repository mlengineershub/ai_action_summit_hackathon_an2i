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

search_proposition_system_prompt = (
    "You are a very helpful Medical AI Assistant. You have been asked to provide medical search propositions based on the conversation between a doctor and a patient."
)

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