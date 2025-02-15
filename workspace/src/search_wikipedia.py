#!/usr/bin/env python3
from typing import Any, Dict, List
import requests


def fetch_wikipedia_extract(pageid: int) -> str:
    """
    Fetch the full extract text for a given Wikipedia page ID using the MediaWiki API.

    Args:
        pageid: The Wikipedia page ID.

    Returns:
        The full extract text (plain text) of the article, or "Not Provided" if unavailable.

    Raises:
        RuntimeError: If the API request fails.
    """
    base_url: str = "https://en.wikipedia.org/w/api.php"
    params: Dict[str, Any] = {
        "action": "query",
        "prop": "extracts",
        "pageids": str(pageid),
        "explaintext": 1,
        "format": "json",
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching Wikipedia extract: {e}") from e

    pages: Dict[str, Any] = data.get("query", {}).get("pages", {})
    page: Dict[str, Any] = pages.get(str(pageid), {})
    extract: str = page.get("extract", "Not Provided")
    return extract


def search_wikipedia(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search Wikipedia for articles related to the research query and retrieve detailed text.

    This function performs two steps:
      1. Uses the MediaWiki API to search for articles matching the query.
      2. For each result, fetches the full extract text using the page ID.

    Args:
        query: The research query string (e.g., "Chest pain without shortness of breath or dizziness").
        limit: Maximum number of search results to retrieve (default is 5).

    Returns:
        A list of dictionaries, each containing:
          - pageid: The Wikipedia page ID.
          - title: The title of the article.
          - snippet: A short snippet from the search result.
          - extract: The full extract text of the article.

    Raises:
        RuntimeError: If an API request fails.
    """
    base_url: str = "https://en.wikipedia.org/w/api.php"
    params: Dict[str, Any] = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Error searching Wikipedia: {e}") from e

    search_results: List[Dict[str, Any]] = data.get("query", {}).get("search", [])
    results: List[Dict[str, Any]] = []
    for item in search_results:
        pageid: int = item.get("pageid", -1)
        title: str = item.get("title", "Not Provided")
        snippet: str = item.get("snippet", "Not Provided")
        extract: str = (
            fetch_wikipedia_extract(pageid) if pageid != -1 else "Not Provided"
        )
        results.append(
            {
                "pageid": pageid,
                "title": title,
                "snippet": snippet,
                "extract": extract,
            }
        )
    return results


def main() -> None:
    query: str = "Chest pain without shortness of breath or dizziness"
    print("Wikipedia Research Query:", query)
    results: List[Dict[str, Any]] = search_wikipedia(query, limit=3)
    for i, res in enumerate(results, start=1):
        print(f"Result {i}:")
        print(f"  Page ID: {res['pageid']}")
        print(f"  Title: {res['title']}")
        print(f"  Snippet: {res['snippet']}")
        # Display a preview (first 200 characters) of the full extract text
        print(f"  Extract (preview): {res['extract'][:1000]}...")
        print("-" * 60)


if __name__ == "__main__":
    main()
