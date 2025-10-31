# job_spy.py — LinkedIn search via python-jobspy
from jobspy import scrape_jobs
import pandas as pd

def get_jobs(search_term: str,
             location: str,
             num_results: int = 5) -> pd.DataFrame:
    """Fetch LinkedIn jobs with python-jobspy."""
    df = scrape_jobs(
        site_name="linkedin",
        search_term=search_term,
        location=location,
        results_wanted=num_results,
        get_skills=False,
    )
    need = ["title", "company", "location", "job_url", "description"]
    for c in need:
        if c not in df.columns:
            df[c] = ""
    return df[need + [c for c in df.columns if c not in need]]

def print_picklist(df: pd.DataFrame):
    print("\nTop Results")
    print("------------------------------------------------------------")
    for i, row in df.head(5).iterrows():
        title = (row.get("title") or "")[:60]
        comp  = (row.get("company") or "")[:40]
        loc   = (row.get("location") or "")[:40]
        print(f"[{i}] {title} — {comp} — {loc}")
    print("------------------------------------------------------------")