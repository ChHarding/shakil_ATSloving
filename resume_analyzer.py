# resume_analyzer functions
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"
client = None

if not USE_MOCK:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("⚠️ Missing OPENAI_API_KEY in .env file")
    client = OpenAI(api_key=api_key)


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