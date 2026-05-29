"""
Film Data Fetcher
=================

Fetches film metadata from Wikipedia.
Falls back gracefully when data is unavailable.
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import quote

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_REST = "https://en.wikipedia.org/api/rest_v1/page/summary"
HEADERS = {"User-Agent": "TopFour/1.0 (film recommender; educational use)"}

EMPTY_RESULT = {
    "title": None,
    "director": None,
    "year": None,
    "summary": "",
    "genres": [],
    "runtime": None,
}


class FilmFetcher:
    """Fetches film metadata from Wikipedia with graceful fallbacks."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_film_data(self, title: str) -> dict:
        """
        Return film metadata dict. Tries Wikipedia first; falls back to empty
        skeleton so callers can always unpack the same keys.
        """
        data = self._scrape_wikipedia(title)
        if not data:
            data = self._search_imdb(title)
        if not data:
            return {**EMPTY_RESULT, "title": title}
        return data

    # ------------------------------------------------------------------
    # Wikipedia
    # ------------------------------------------------------------------

    def _scrape_wikipedia(self, title: str) -> dict:
        """Fetch and parse film data from Wikipedia. Returns {} on failure."""
        page_title = self._find_wikipedia_page(title)
        if not page_title:
            return {}

        summary = self._get_wikipedia_summary(page_title)
        infobox = self._parse_infobox(page_title)

        return {
            "title": title,
            "director": infobox.get("director"),
            "year": infobox.get("year"),
            "summary": summary,
            "genres": infobox.get("genres", []),
            "runtime": infobox.get("runtime"),
        }

    def _find_wikipedia_page(self, title: str) -> Optional[str]:
        """
        Search Wikipedia for the film. Returns the best-matching page title,
        preferring results that explicitly include the search title.
        """
        params = {
            "action": "query",
            "list": "search",
            "srsearch": f"{title} film",
            "srlimit": 5,
            "format": "json",
        }
        try:
            resp = self.session.get(WIKIPEDIA_API, params=params, timeout=10)
            resp.raise_for_status()
            results = resp.json().get("query", {}).get("search", [])
        except Exception:
            return None

        if not results:
            return None

        title_lower = title.lower()
        for result in results:
            if title_lower in result["title"].lower():
                return result["title"]
        return results[0]["title"]

    def _get_wikipedia_summary(self, page_title: str) -> str:
        """Fetch the introductory extract via the Wikipedia REST summary API."""
        url = f"{WIKIPEDIA_REST}/{quote(page_title.replace(' ', '_'))}"
        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json().get("extract", "")
        except Exception:
            return ""

    def _parse_infobox(self, page_title: str) -> dict:
        """Fetch page HTML and extract structured fields from the film infobox."""
        params = {
            "action": "parse",
            "page": page_title,
            "prop": "text",
            "format": "json",
        }
        try:
            resp = self.session.get(WIKIPEDIA_API, params=params, timeout=15)
            resp.raise_for_status()
            html = resp.json().get("parse", {}).get("text", {}).get("*", "")
        except Exception:
            return {}

        soup = BeautifulSoup(html, "html.parser")
        infobox = soup.find("table", class_=lambda c: c and "infobox" in c)
        if not infobox:
            return {}

        result = {}
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if not th or not td:
                continue
            label = th.get_text(strip=True).lower()

            if "directed" in label:
                items = self._extract_list(td)
                result["director"] = items[0] if items else None

            elif "release" in label and "year" not in result:
                year = self._extract_year(td.get_text())
                if year:
                    result["year"] = year

            elif "running time" in label or "runtime" in label:
                result["runtime"] = self._extract_runtime(td.get_text())

            elif "genre" in label:
                result["genres"] = self._extract_list(td)

        return result

    # ------------------------------------------------------------------
    # IMDb (no public API key available — stub for future use)
    # ------------------------------------------------------------------

    def _search_imdb(self, title: str) -> dict:
        """IMDb lookup stub — requires an API key not currently configured."""
        return {}

    # ------------------------------------------------------------------
    # Text helpers
    # ------------------------------------------------------------------

    def _clean_text(self, text: str) -> str:
        """Strip citation brackets and collapse whitespace."""
        text = re.sub(r'\[.*?\]', '', text)
        return " ".join(text.split())

    def _extract_year(self, text: str) -> Optional[int]:
        match = re.search(r'\b(19|20)\d{2}\b', text)
        return int(match.group()) if match else None

    def _extract_runtime(self, text: str) -> Optional[int]:
        match = re.search(r'(\d+)\s*min', text, re.IGNORECASE)
        return int(match.group(1)) if match else None

    def _extract_list(self, td) -> list:
        """Extract items from a td — handles <li>, <a>, and plain text."""
        items = [li.get_text(strip=True) for li in td.find_all("li")]
        if items:
            return [self._clean_text(i) for i in items if i]
        items = [a.get_text(strip=True) for a in td.find_all("a")]
        if items:
            return [self._clean_text(i) for i in items if i]
        text = self._clean_text(td.get_text())
        return [text] if text else []
