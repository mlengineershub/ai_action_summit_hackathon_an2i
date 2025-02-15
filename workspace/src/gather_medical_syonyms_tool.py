#!/usr/bin/env python3
from typing import Any, Dict, List, Optional
import requests


def search_medical_conditions_with_details(query: str, count: int = 7, offset: int = 0) -> Dict[str, Any]:
    """
    Search the Clinical Table Search Service API for medical conditions using the provided query.
    
    This function uses the following query parameters:
      - terms: the search terms (e.g., "Chest pain without shortness of breath or dizziness")
      - count: number of results to retrieve
      - offset: starting result number (0-based)
      - df: display fields (here, ICD-9 code and primary name)
      - ef: extra field to retrieve detailed descriptive text ("term_icd9_text")
    
    The API returns a list with the following elements:
      [ total_results, codes, extra_data, display, code_system (optional) ]
    
    Args:
        query: The search string for medical conditions.
        count: Number of results to retrieve (default 7).
        offset: Starting offset for results (default 0).
    
    Returns:
        A dictionary with keys:
          "total": total number of results,
          "codes": list of codes,
          "extra": extra fields (e.g., "term_icd9_text"),
          "display": list of display arrays,
          "code_system": optional code system information.
    
    Raises:
        RuntimeError: If there is an error accessing the API.
    """
    base_url: str = "https://clinicaltables.nlm.nih.gov/api/conditions/v3/search"
    params: Dict[str, Any] = {
        "terms": query,
        "count": count,
        "offset": offset,
        "df": "term_icd9_code,primary_name",
        "ef": "term_icd9_text",
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data: List[Any] = response.json()
    except requests.RequestException as err:
        raise RuntimeError(f"Error while accessing the API: {err}") from err
    
    result: Dict[str, Any] = {
        "total": data[0],
        "codes": data[1],
        "extra": data[2],
        "display": data[3],
        "code_system": data[4] if len(data) > 4 else None,
    }
    return result


query: str = "Gastroenteritis"
results: Dict[str, Any] = search_medical_conditions_with_details(query)

total: int = results["total"]
print("Total Results:", total)

# 'extra' is a dict with key "term_icd9_text" mapping to a list of strings (one per result)
extra_texts: List[str] = results["extra"].get("term_icd9_text", [])
display: List[List[str]] = results["display"]
codes: List[str] = results["codes"]

# Iterate through results using index to match extra details
for i, code in enumerate(codes):
    # Each display entry is expected to be a list, where the second element is the condition's name
    condition: str = display[i][1] if i < len(display) and len(display[i]) > 1 else "Not Provided"
    detail: str = extra_texts[i] if i < len(extra_texts) else "Not Provided"
    print(f"Code: {code}, Condition: {condition}, Details: {detail}")

