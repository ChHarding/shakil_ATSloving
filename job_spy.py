# jobspy.py
"""
Minimal JobSpy integration for ResumeSync (v1).
Searches LinkedIn and returns a tidy DataFrame.
"""

from jobspy import scrape_jobs
import pandas as pd

def get_jobs(search_term="UX Designer", location="United States", num_results=10, fetch_description=False) -> pd.DataFrame:
    print(f"🔍 Searching LinkedIn for '{search_term}' in {location} …")
    try:
        df = scrape_jobs(
            site_name=["linkedin"],
            search_term=search_term,
            location=location,
            results_wanted=num_results,
            linkedin_fetch_description=fetch_description,  # False = fast (no descriptions)
        )
        if df.empty:
            print("⚠️ No jobs found.")
            return pd.DataFrame()
        keep = [c for c in ["title","company","location","job_url","date_posted","description"] if c in df.columns]
        print(f"✅ Found {len(df)} jobs.")
        return df[keep].copy()
    except Exception as e:
        print("❌ JobSpy error:", e)
        return pd.DataFrame()

def print_picklist(df: pd.DataFrame, top_n: int = 10) -> None:
    print("\n📋 Top Results")
    print("-" * 60)
    for i, row in df.head(top_n).iterrows():
        print(f"[{i}] {row.get('title','?')} — {row.get('company','?')} — {row.get('location','?')}")
    print("-" * 60)