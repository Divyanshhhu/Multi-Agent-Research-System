from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import os
import streamlit as st

load_dotenv()


# ==========================================
# Safe Secret Getter
# ==========================================

def get_secret(key, default=None):

    value = os.getenv(key)

    if value:
        return value

    try:
        return st.secrets[key]
    except:
        return default


# ==========================================
# Tavily Client
# ==========================================

TAVILY_API_KEY = get_secret("TAVILY_API_KEY")

tavily = TavilyClient(TAVILY_API_KEY)



# ==========================================
# Search Tool
# ==========================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.
    Returns titles, URLs and snippets.
    """

    try:
        results = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        output = []

        for idx, result in enumerate(results["results"], start=1):

            output.append(
                f"""
Result {idx}

Title:
{result['title']}

URL:
{result['url']}

Snippet:
{result['content'][:400]}
"""
            )

        return "\n" + ("=" * 60).join(output)

    except Exception as e:
        return f"Search Error: {str(e)}"


# ==========================================
# Web Scraper Tool
# ==========================================

@tool
def web_scrape(url: str) -> str:
    """
    Scrape and extract text content from a webpage.
    """

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove unwanted elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if len(text) == 0:
            return "No useful content found."

        return text[:5000]

    except Exception as e:
        return f"Scraping Error: {str(e)}"