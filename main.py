# main.py — ResumeSync (LinkedIn + Resume Match)
# Author: Shamim Shakil

import json
from job_spy import get_jobs, print_picklist
from job_detail import fetch_job_description
from resume_reader import read_resume_text
from resume_analyzer import analyze_resume_match


def normalize_ai_result(result):
    """Ensure analyzer output is a dict with expected keys."""
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except Exception:
            return {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "summary": result.strip(),
            }

    return {
        "match_score": int(result.get("match_score", 0) or 0),
        "matched_skills": list(result.get("matched_skills", []) or []),
        "missing_skills": list(result.get("missing_skills", []) or []),
        "summary": str(result.get("summary", "") or "").strip(),
    }


def offer_resume_analysis(jd_text: str):
    """Prompt user to analyze a resume against the given JD text."""
    if not jd_text or jd_text.startswith("[No description"):
        return

    choice = input("\nAnalyze your resume against this job? (y/n): ").strip().lower()
    if choice != "y":
        return

    path = input("Enter resume path (.pdf/.docx/.txt): ").strip()
    if not path:
        print("No file provided. Skipping analysis.")
        return

    try:
        resume_text = read_resume_text(path)
    except Exception as e:
        print(f"Error reading resume: {e}")
        return

    print("\nAnalyzing resume vs job description...\n")
    try:
        raw = analyze_resume_match(resume_text, jd_text)
        result = normalize_ai_result(raw)
    except Exception as e:
        print(f"Analysis failed: {e}")
        return

    print(f"Match Score: {result['match_score']}%")
    print("Matched Skills:", ", ".join(result["matched_skills"]) or "—")
    print("Missing Skills:", ", ".join(result["missing_skills"]) or "—")
    if result["summary"]:
        print("\nSummary:")
        print(result["summary"])
    print("\n" + "-" * 60 + "\n")


def search_flow():
    """Browse LinkedIn jobs and fetch full descriptions."""
    role = input("Job title (e.g., UX Researcher): ").strip() or "UX Designer"
    loc = input("Location (e.g., United States): ").strip() or "United States"

    print("\nSearching LinkedIn jobs...\n")
    try:
        jobs = get_jobs(role, loc, num_results=5)
    except Exception as e:
        print(f"Search failed: {e}")
        return

    if jobs.empty:
        print("No results. Try a broader term/location.\n")
        return

    while True:
        print_picklist(jobs)
        choice = input("Pick a job number (0–4), 'new' for new search, or 'exit': ").strip().lower()

        if choice in ("exit", "", "q"):
            print("Goodbye!\n")
            return
        if choice == "new":
            print()
            return
        if not choice.isdigit():
            print("Enter a number (0–4), 'new', or 'exit'.\n")
            continue

        idx = int(choice)
        if idx < 0 or idx >= len(jobs):
            print("Out of range. Pick one of the shown numbers.\n")
            continue

        row = jobs.iloc[idx]
        print("\n— Job Detail —")
        print(f"Title   : {row.get('title')}")
        print(f"Company : {row.get('company')}")
        print(f"Location: {row.get('location')}")
        print(f"URL     : {row.get('job_url')}\n")

        print("Fetching full job description...")
        jd_text = fetch_job_description(row.get("job_url", "")) or "[No description available — page may be private.]"

        print("\nFull Job Description\n")
        print(jd_text)
        print("\n" + "-" * 60 + "\n")

        offer_resume_analysis(jd_text)


def url_flow():
    """Paste a public LinkedIn URL, fetch its description, then analyze resume."""
    url = input("Paste a LinkedIn public job URL: ").strip()
    if not url:
        print("URL cannot be empty.")
        return

    print("\nFetching full job description...\n")
    jd_text = fetch_job_description(url) or "[No description available — page may be private.]"

    print("Full Job Description\n")
    print(jd_text)
    print("\n" + "-" * 60 + "\n")

    offer_resume_analysis(jd_text)


def main():
    print("\nResumeSync — LinkedIn Job + Resume Match\n")
    while True:
        print("1) Browse LinkedIn Jobs (via JobSpy)")
        print("2) Paste LinkedIn Public Job URL")
        print("3) Exit")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            search_flow()
        elif choice == "2":
            url_flow()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please select 1–3.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.\n")
        