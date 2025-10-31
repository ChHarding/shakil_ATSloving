# job_detail.py — LinkedIn public (guest) description fetcher
import re
import requests
from bs4 import BeautifulSoup
from user_agents import get_random_headers

MAX_CHARS = 100_000  # allow long descriptions

def _clean(txt: str) -> str:
    return re.sub(r"\s+", " ", (txt or "")).strip()

def _extract_text_from_soup(soup: BeautifulSoup) -> str:
    """Try common LinkedIn job description containers."""
    selectors = [
        '[data-test-description-section]',
        'div.show-more-less-html__markup',
        'div.description__text',
        'section.description',
        'div#job-details',
        'article',
    ]
    for sel in selectors:
        node = soup.select_one(sel)
        if node:
            return _clean(node.get_text(" ", strip=True))
    paras = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    if paras:
        longest = max(paras, key=len)
        if len(longest) > 100:
            return _clean(longest)
    return ""

def _linkedin_job_id(url: str) -> str:
    """Extract the numeric job ID from a LinkedIn job URL."""
    m = re.search(r"/jobs/view/(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/view/(\d+)", url)
    return m.group(1) if m else ""

def _fetch_linkedin_guest(url: str, timeout: int = 15) -> str:
    """Fetch job description from LinkedIn's public guest API."""
    job_id = _linkedin_job_id(url)
    if not job_id:
        return ""
    api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    r = requests.get(api_url, headers=get_random_headers(), timeout=timeout)
    if r.status_code != 200 or not r.text:
        return ""
    soup = BeautifulSoup(r.text, "lxml")
    txt = _extract_text_from_soup(soup)
    return txt[:MAX_CHARS] if txt else ""

def _fetch_linkedin_canonical(url: str, timeout: int = 15) -> str:
    """Fallback: fetch the actual job posting page HTML."""
    headers = get_random_headers()
    headers["Referer"] = "https://www.google.com/"
    r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
    if r.status_code != 200 or not r.text:
        return ""
    soup = BeautifulSoup(r.text, "lxml")
    txt = _extract_text_from_soup(soup)
    return txt[:MAX_CHARS] if txt else ""

def fetch_job_description(url: str, timeout: int = 15) -> str:
    """Main entry: try guest API, then canonical HTML fallback."""
    if not url or "linkedin.com" not in url.lower():
        return ""
    txt = _fetch_linkedin_guest(url, timeout=timeout)
    if txt:
        return txt
    return _fetch_linkedin_canonical(url, timeout=timeout)