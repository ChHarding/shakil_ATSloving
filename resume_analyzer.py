# resume_analyzer functions
import os
import json
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def _get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Look up secrets from env vars first, then Streamlit secrets if available."""
    val = os.getenv(key)
    if val:
        return str(val)

    try:
        import streamlit as st  # type: ignore

        secrets = st.secrets or {}
        if key in secrets:
            return str(secrets[key])
        # allow nested grouping e.g. st.secrets["api_keys"]["openai"]
        if isinstance(secrets, dict):
            for sub in secrets.values():
                if isinstance(sub, dict) and key in sub:
                    return str(sub[key])
    except Exception:
        pass

    return default


USE_MOCK = str(_get_secret("USE_MOCK", "false")).lower() == "true"
_client: Optional[OpenAI] = None


def _require_client() -> OpenAI:
    """Create the OpenAI client lazily so it works in CLI + Streamlit."""
    global _client
    if _client:
        return _client

    api_key = _get_secret("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("⚠️ Missing OPENAI_API_KEY. Set it in .env or Streamlit secrets.")

    _client = OpenAI(api_key=api_key)
    return _client


def analyze_resume_match(resume_text: str, job_text: str):
    """Analyze how well a resume matches a job description."""
    if USE_MOCK:
        # fallback for classmates/instructors without API keys
        return {
            "match_score": 75,
            "matched_skills": ["UX Research", "Prototyping", "Figma"],
            "missing_skills": ["WCAG", "Design Systems"],
            "summary": "Mock analysis — replace with real OpenAI key for live scoring."
        }

    prompt = f"""
    You are an assistant evaluating job fit.
    Compare this RESUME and JOB DESCRIPTION.
    Return JSON with keys: match_score (0–100), matched_skills, missing_skills, summary.

    RESUME:
    {resume_text[:4000]}

    JOB DESCRIPTION:
    {job_text[:4000]}
    """

    client = _require_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=400
    )

    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except Exception:
        return {"summary": text, "match_score": 0}
