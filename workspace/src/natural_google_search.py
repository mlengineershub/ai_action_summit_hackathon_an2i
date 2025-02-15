import requests
from googlesearch import search
from bs4 import BeautifulSoup
from typing import Any
from workspace.src.utils import initialize_client, generate_prompt, generate_response
from workspace.src.prompts import (
    summarize_google_research_prompt_template,
    summarize_google_research_system_prompt,
)
from openai import OpenAI


# --- Web Search Tool ---
def fetch_page_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            return soup.get_text(separator="\n", strip=True)
        else:
            return f"Error: Received status code {response.status_code} for URL {url}"
    except Exception as e:
        return f"Error fetching {url}: {e}"


def web_search(query: str) -> dict[str, Any]:
    urls = list(search(query, num_results=1))
    if not urls:
        return {"content": "No results found for query."}
    results = []
    for url in urls:
        text = fetch_page_text(url)
        results.append(f"Content from {url}:\n{text}\n{'=' * 80}")
    return {"content": "\n\n".join(results)}


def summarize_google_research(client: OpenAI, search_query: str) -> str:
    # search the web and prepare google search results
    search_results = web_search(search_query)
    prompt = generate_prompt(
        summarize_google_research_prompt_template,
        google_search_results=search_results["content"],
    )
    system_prompt = summarize_google_research_system_prompt
    response: str = generate_response(
        client=client, system_prompt=system_prompt, user_prompt=prompt
    )
    return response


# # Example usage: ======================================== (will be removed)

client = initialize_client()
search_query = "COVID-19 symptoms"
response = summarize_google_research(client, search_query=search_query)
print(response)
