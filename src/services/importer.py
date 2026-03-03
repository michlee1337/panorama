"""
Service for importing articles/webpages and extracting structured artifact data.

Functions:
    fetch_page(url) -> dict
    extract_artifact_data(url) -> dict
"""

import json
import os
import re
from urllib.parse import urlparse

import anthropic
import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    """
    Fetches a webpage and extracts its text content.

        Parameters:
            url (str): The URL to fetch

        Returns:
            dict: {title, text, url, source_name}
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove script/style elements
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    # Extract main content text
    text = soup.get_text(separator="\n", strip=True)
    # Collapse excessive whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Derive source name from domain
    parsed = urlparse(url)
    source_name = parsed.netloc.replace("www.", "")

    return {
        "title": title,
        "text": text[:15000],  # cap to avoid huge payloads
        "url": url,
        "source_name": source_name,
    }


def extract_artifact_data(url):
    """
    Fetches a URL and uses Claude to extract structured artifact data.

        Parameters:
            url (str): The URL of the article/webpage

        Returns:
            dict: Structured artifact data with keys:
                - title (str)
                - description (str)
                - concept (str): main concept
                - prerequisites (list[str]): prerequisite concept names
                - chunks (list[dict]): each with {concept, title, content}
                - mediatype (int): 0=Unknown, 1=Text, 2=Video, 3=Other
                - duration (int): 0=Unknown, 1=Minutes, 2=Days, 3=Months
                - source_name (str)
                - source_link (str)
    """
    page = fetch_page(url)

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Analyze this article/webpage and extract structured learning resource metadata.

Title: {page['title']}
Source: {page['source_name']}
URL: {page['url']}

Content:
{page['text']}

---

Return a JSON object with exactly these fields:

{{
  "title": "A concise, descriptive title for this learning resource",
  "description": "A 1-3 sentence summary of what the reader will learn",
  "concept": "The single main concept/topic this resource teaches (lowercase)",
  "prerequisites": ["list", "of", "prerequisite", "concepts", "needed to understand this resource (lowercase)"],
  "chunks": [
    {{
      "concept": "sub-concept covered in this section (lowercase)",
      "title": "Section title",
      "content": "Brief summary of this section's key points"
    }}
  ],
  "mediatype": 1,
  "duration": 1
}}

Rules:
- "concept" should be a single, specific topic name (e.g. "neural networks", "recursion", "supply chain management")
- "prerequisites" should be foundational concepts someone needs before reading this (empty list if none)
- "chunks" should break the article into 2-6 logical sections, each with its own sub-concept
- "mediatype": 1 for text articles/blogs, 2 for video content, 3 for other (podcasts, interactive, etc.), 0 if unclear
- "duration": 1 for content consumable in minutes, 2 for content taking days, 3 for content taking months, 0 if unclear
- All concept names should be lowercase
- Return ONLY valid JSON, no other text"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    response_text = message.content[0].text.strip()

    # Extract JSON from response (handle markdown code blocks)
    json_match = re.search(r"```(?:json)?\s*(.*?)```", response_text, re.DOTALL)
    if json_match:
        response_text = json_match.group(1).strip()

    data = json.loads(response_text)

    # Attach source info
    data["source_name"] = page["source_name"]
    data["source_link"] = page["url"]

    return data
