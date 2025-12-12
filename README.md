# shakil_ResumeSync
ResumeSync helps UX designers and other job seekers analyze how well their resumes match job descriptions.  
It uses **JobSpy** to fetch real job postings from LinkedIn and prepares the data for intelligent comparison (via the OpenAI API in later versions).

---

## Project Overview

**Developer:** Shamim Shakil  
**Course:** HCI 584 — Human–Computer Interaction  
**Instructor:** Dr. Chris Harding  
**Version:** 1.0 (Progress Report A)

This tool forms the foundation of a larger system that will:
1. Scrape live job postings using JobSpy.
2. Compare resumes with job descriptions using the OpenAI API.
3. Provide data-driven match scores, keyword gaps, and improvement suggestions.

---

## Current Features (Version 1)

✅ Set up complete GitHub project structure with:
- `main.py` — program entry point  
- `jobspy.py` — handles job search via LinkedIn using JobSpy  
- `requirements.txt` — lists dependencies for easy setup  
- `Docs/` — contains project specification and design artifacts  

✅ Implemented JobSpy integration:
- Dynamically searches job titles and locations.
- Returns job title, company, location, and job URL.
- Displays results in a readable picklist in the terminal.

✅ Established clean repo structure:
- `.gitignore`, `LICENSE`, and `README.md` in root.
- All `.py` files remain in the project root for easy importing.
- Documentation stored inside `Docs/` folder.

---

## Deploying the Streamlit Web App

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Create a `.env` (local testing) or `.streamlit/secrets.toml` (Streamlit Cloud) with**
   ```toml
   OPENAI_API_KEY = "sk-..."
   USE_MOCK = "false"  # set to "true" to disable OpenAI calls
   ```
   A sample template lives at `.streamlit/secrets_template.toml`.
3. **Run locally**
   ```bash
   streamlit run app.py
   ```
   The UI lets you search LinkedIn via JobSpy, fetch job descriptions, upload a resume PDF, and invoke `resume_analyzer`.
4. **Deploy on Streamlit Cloud**
   - Push this repo to GitHub.
   - In Streamlit Cloud, create a new app pointing to `app.py`.
   - Paste the same secrets in the dashboard (`Settings → Secrets`).
   - (Optional) keep `USE_MOCK="true"` for demos without an API key.

The `job_spy.py` and `job_detail.py` modules rely on live LinkedIn scraping. If LinkedIn rate-limits Streamlit Cloud, switch to cached sample jobs or your own API backend for reliability.
