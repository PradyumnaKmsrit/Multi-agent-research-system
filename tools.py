from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import os
from dotenv import load_dotenv
from rich import print
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def _search_with_retry(query: str, max_results: int = 5):
    with DDGS(timeout=15) as ddgs:
        return list(ddgs.text(query, max_results=max_results, backend="duckduckgo"))

@tool
def duckduckgo_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
    try:
        results = _search_with_retry(query)
    except Exception as e:
        return f"Search failed after retries: {str(e)}"

    out = []
    for r in results:
        out.append(
            f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body'][:300]}\n"
        )

    return "\n----\n".join(out)

@tool
def fetch_and_clean_page(url: str) -> str:
    """Fetch a webpage by URL and return its clean, readable text content for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"


if __name__ == "__main__":
    print(duckduckgo_search.invoke({"query": "latest AI news"}))