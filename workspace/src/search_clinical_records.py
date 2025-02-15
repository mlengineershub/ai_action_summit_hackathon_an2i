#!/usr/bin/env python3
from typing import Any, Dict, List
import requests


def search_clinical_conditions(
    query: str, count: int = 5, offset: int = 0
) -> Dict[str, Any]:
    """
    Search the Clinical Table Search Service API for medical conditions based on a research query.

    This function sends a GET request to the API endpoint with the following parameters:
      - terms: the search query (e.g., "Chest pain without shortness of breath or dizziness")
      - count: number of results to retrieve
      - offset: starting offset for pagination
      - df: display fields ("term_icd9_code,primary_name")
      - ef: extra fields for additional context ("term_icd9_text,synonyms")

    The API returns a list with the following elements:
      [ total_results, codes, extra_data, display, code_system (optional) ]

    Returns:
        A dictionary with keys:
          "total": total number of results,
          "codes": list of codes,
          "extra": dictionary with extra fields data,
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
        "ef": "term_icd9_text,synonyms",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data: List[Any] = response.json()
    except requests.RequestException as e:
        raise RuntimeError(
            f"Error accessing Clinical Table Search Service API: {e}"
        ) from e

    result: Dict[str, Any] = {
        "total": data[0],
        "codes": data[1],
        "extra": data[2],
        "display": data[3],
        "code_system": data[4] if len(data) > 4 else None,
    }
    return result


def main() -> None:
    query: str = "Chest pain"
    results: Dict[str, Any] = search_clinical_conditions(query, count=5)

    print("Clinical Table Search Service Results:")
    print(f"Total Results: {results['total']}")

    codes: List[str] = results["codes"]
    display: List[List[str]] = results["display"]
    extra: Dict[str, Any] = results["extra"]

    # Extract extra context details if available
    term_texts: List[str] = extra.get("term_icd9_text", [])
    synonyms: List[str] = extra.get("synonyms", [])

    for i, code in enumerate(codes):
        primary_name: str = (
            display[i][1]
            if i < len(display) and len(display[i]) > 1
            else "Not Provided"
        )
        detail_text: str = term_texts[i] if i < len(term_texts) else "Not Provided"
        synonym_text: str = synonyms[i] if i < len(synonyms) else "Not Provided"
        print(f"Result {i + 1}:")
        print(f"  Code: {code}")
        print(f"  Primary Name: {primary_name}")
        print(f"  Detailed Text: {detail_text}")
        print(f"  Synonyms: {synonym_text}")
        print("-" * 60)


if __name__ == "__main__":
    main()
