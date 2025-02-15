import requests
from bs4 import BeautifulSoup
from typing import TypedDict, Any
from openai import OpenAI
from workspace.src.prompts import summarize_search_system_prompt, summarize_search_prompt_template
from workspace.src.utils import generate_structured_response, generate_prompt, initialize_client
from workspace.src.pydantic_models import SearchSummary

# Define TypedDicts for better type checking
class Article(TypedDict):
    pmid: str
    title: str
    pubdate: str
    source: str
    summary: str

class SearchResult(TypedDict):
    query: str
    num_articles_found: int
    articles: list[Article]

def search_medical_articles(query: str, retmax: int = 5) -> SearchResult:
    """
    Search for medical articles on PubMed using a research query and return context details.
    
    Parameters:
        query (str): The medical research query.
        retmax (int): The maximum number of articles to retrieve (default is 5).
    
    Returns:
        SearchResult: A dictionary containing the original query, number of articles found, and a list of articles.
    """
    # Define the base URL for PubMed E-utilities
    esearch_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esearch_params: dict[str, Any] = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json"
    }
    
    # Call ESearch to get a list of PMIDs for the query
    esearch_response: requests.Response = requests.get(esearch_url, params=esearch_params)
    if esearch_response.status_code != 200:
        raise Exception(f"ESearch API error: {esearch_response.status_code}")
    search_data: dict[str, Any] = esearch_response.json()
    pmids: list[str] = search_data.get("esearchresult", {}).get("idlist", [])
    
    if not pmids:
        return {"query": query, "num_articles_found": 0, "articles": []}
    
    # Use ESummary to get detailed information about the retrieved PMIDs
    esummary_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    esummary_params: dict[str, Any] = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json"
    }
    esummary_response: requests.Response = requests.get(esummary_url, params=esummary_params)
    if esummary_response.status_code != 200:
        raise Exception(f"ESummary API error: {esummary_response.status_code}")
    summary_data: dict[str, Any] = esummary_response.json()
    
    articles: list[Article] = []
    uids: list[str] = summary_data.get("result", {}).get("uids", [])
    for pmid in uids:
        article_data: dict[str, Any] = summary_data["result"].get(pmid, {})
        article: Article = {
            "pmid": pmid,
            "title": article_data.get("title", "No Title"),
            "pubdate": article_data.get("pubdate", "No Date"),
            "source": article_data.get("source", "No Source"),
            "summary": article_data.get("summary", "")
        }
        articles.append(article)
    
    return {"query": query, "num_articles_found": len(articles), "articles": articles}

def fetch_article_abstract(pmid: str) -> str:
    """
    Fetch the abstract text for a given PubMed ID (PMID) using the EFetch API.

    Parameters:
        pmid (str): The PubMed ID of the article.

    Returns:
        str: The abstract text, or a message if not available.
    """
    efetch_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params: dict[str, Any] = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response: requests.Response = requests.get(efetch_url, params=params)
    if response.status_code != 200:
        return f"EFetch API error: {response.status_code}"
    
    # Parse the XML response using BeautifulSoup
    soup: BeautifulSoup = BeautifulSoup(response.content, "lxml")
    abstract_tags = soup.find_all("abstracttext")
    if not abstract_tags:
        return "No abstract available."
    
    # Combine all parts of the abstract if there are multiple tags
    abstract: str = " ".join(tag.get_text() for tag in abstract_tags)
    return abstract.strip()

def generate_search_summary(client: OpenAI, prompt: str) -> dict[str, Any]:
    system_prompt = summarize_search_system_prompt
    response: dict[str, Any] = generate_structured_response(
        client, system_prompt, prompt, SearchSummary
    )
    return response

# Example usage:
if __name__ == '__main__':
    client = initialize_client()
    query: str = "chest pain without shortness of breath"
    result: SearchResult = search_medical_articles(query)
    
    # Gather all abstracts into one big string
    content_article: str = ""
    for article in result["articles"]:
        abstract: str = fetch_article_abstract(article["pmid"])
        content_article += f"PMID {article['pmid']} - {article['title']}:\n{abstract}\n\n"
    
    print("Combined Article Content:\n")
    print(content_article)
    # create a mock summary of a patient condition that is related to chest pain 
    patient_condition = """The patient is a 45-year and has been experiencing chest pain without shortness of breath for the past 2 days. The pain is described as sharp and localized on the left side of the chest. The patient has no history of heart conditions or high blood pressure. The pain is not aggravated by physical activity or relieved by rest. The patient has not taken any medication for the pain."""
    prompt = generate_prompt(prompt_template=summarize_search_prompt_template, patient_condition=patient_condition ,medical_articles=content_article)
    response = generate_search_summary(client, prompt)
