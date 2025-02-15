# #!/usr/bin/env python3
# from typing import Set
# import re
# import requests
# from bs4 import BeautifulSoup


# def search_mayo_clinic(query: str) -> str:
#     """
#     Search Mayo Clinic for a given medical research query and aggregate text
#     from the resulting articles.

#     This function performs the following steps:
#       1. Constructs the search URL for Mayo Clinic using the query.
#       2. Parses the search results page to extract article links.
#       3. Visits each article link, extracts the main text content.
#       4. Aggregates the text from all articles into a single string.

#     Args:
#         query: The research query string (e.g., "chest pain").

#     Returns:
#         A single string containing the concatenated text from all found articles.

#     Raises:
#         RuntimeError: If an error occurs during HTTP requests.
#     """
#     headers = {"User-Agent": "Mozilla/5.0 (compatible; Python script)"}
#     base_search_url = "https://www.mayoclinic.org/diseases-conditions/search-results?q="
#     search_url = base_search_url + query.replace(" ", "+")

#     try:
#         search_resp = requests.get(search_url, headers=headers)
#         search_resp.raise_for_status()
#     except requests.RequestException as e:
#         raise RuntimeError(f"Error fetching Mayo Clinic search results: {e}") from e

#     search_soup = BeautifulSoup(search_resp.text, "html.parser")

#     # Extract links from search results. We assume article URLs start with "/diseases-conditions/"
#     link_pattern = re.compile(r"^/diseases-conditions/.*")
#     links: Set[str] = set()
#     for a in search_soup.find_all("a", href=True):
#         href = a["href"]
#         if link_pattern.match(href) and "search-results" not in href:
#             full_url = "https://www.mayoclinic.org" + href
#             links.add(full_url)

#     aggregated_text = ""
#     for url in links:
#         try:
#             article_resp = requests.get(url, headers=headers)
#             article_resp.raise_for_status()
#         except requests.RequestException:
#             continue

#         article_soup = BeautifulSoup(article_resp.text, "html.parser")
#         article_text = ""

#         # Attempt to locate common containers for the article's main text.
#         # This may vary by page; we try a few common patterns.
#         content_div = article_soup.find("div", class_="content")
#         if content_div:
#             article_text = content_div.get_text(separator="\n", strip=True)
#         else:
#             article_tag = article_soup.find("article")
#             if article_tag:
#                 article_text = article_tag.get_text(separator="\n", strip=True)

#         # Fallback: get all text from the page.
#         if not article_text:
#             article_text = article_soup.get_text(separator="\n", strip=True)

#         aggregated_text += f"URL: {url}\n{article_text}\n\n{'-' * 80}\n\n"

#     return aggregated_text


# def main() -> None:
#     query: str = "chest pain"
#     result_text: str = search_mayo_clinic(query)
#     print("Aggregated Article Text:")
#     print(result_text)


# if __name__ == "__main__":
#     main()
