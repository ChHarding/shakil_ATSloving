# main.py - ResumeSync CLI Prototype (Version 1 Progress Report A)
# Author: Shamim Shakil

from job_spy import get_jobs, print_picklist

def main():
    print("=== ResumeSync — Basic Job Search (v1) ===")
    role = input("Job title (e.g., UX Researcher): ").strip() or "UX Designer"
    loc  = input("Location (e.g., United States): ").strip() or "United States"

    jobs = get_jobs(role, loc, num_results=5, fetch_description=False)
    if jobs.empty:
        return

    print_picklist(jobs)

    selection = input("\nPick a job number to view details (or Enter to exit): ").strip()
    if not selection.isdigit():
        print("Bye!"); return

    idx = int(selection)
    if idx < 0 or idx >= len(jobs):
        print("Invalid number."); return

    row = jobs.iloc[idx]
    print("\n—— Selected Job ——")
    print("Title   :", row.get("title"))
    print("Company :", row.get("company"))
    print("Location:", row.get("location"))
    print("URL     :", row.get("job_url"))

    desc = row.get("description")
    if desc:
        print("\n(Description preview)")
        print(desc[:600], "..." if len(desc) > 600 else "")
    else:
        print("\n(No description fetched — enable fetch_description=True later for full text.)")

if __name__ == "__main__":
    main()