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
