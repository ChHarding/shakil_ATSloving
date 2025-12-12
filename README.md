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

## Running Locally (macOS / Linux / Windows)

1. **Clone & create a virtual environment**
   ```bash
   git clone https://github.com/<you>/shakil_ResumeSync.git
   cd shakil_ResumeSync
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Configure secrets**
   ```bash
   cp .streamlit/secrets_template.toml .env        # for CLI + local testing
   cp .streamlit/secrets_template.toml .streamlit/secrets.toml  # for Streamlit local runs
   ```
   Edit either file and set
   ```toml
   OPENAI_API_KEY = "sk-your-key"
   USE_MOCK = "false"  # set to "true" to skip real OpenAI calls
   ```
4. **Launch Streamlit**
   ```bash
   streamlit run app.py
   ```
   Visit the displayed URL (usually http://localhost:8501), search jobs, upload a resume PDF, and view the AI match analysis. Stop with `Ctrl+C`.

If you do not have an OpenAI key, set `USE_MOCK="true"` so the analyzer returns a placeholder result instead of failing.

## Deploying on Streamlit Cloud (Free Tier)

1. Push this repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and click **New app**.
3. Select the repo/branch and set the entry point to `app.py`.
4. Under **Settings → Secrets**, paste the contents of `.streamlit/secrets_template.toml` with your real key:
   ```toml
   OPENAI_API_KEY = "sk-your-key"
   USE_MOCK = "false"
   ```
5. Click **Deploy**. Streamlit Cloud installs `requirements.txt`, runs `streamlit run app.py`, and exposes the public URL automatically.
6. Test both tabs (search + direct URL). Watch the app logs for LinkedIn scraping or OpenAI issues. If LinkedIn blocks the guest scraping endpoints, consider switching `USE_MOCK="true"` or caching known job descriptions for demos.

The `job_spy.py` and `job_detail.py` modules rely on live LinkedIn scraping. Network blocks or rate limits are possible on Streamlit Cloud—fall back to cached/sample data or your own proxy service when reliability is critical.
