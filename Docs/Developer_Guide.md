# Developer's Guide for ResumeSync

## Overview

ResumeSync is a Python-based tool designed to help job seekers evaluate how well their resumes align with job postings, particularly in fields like UX design. It fetches real-time job listings from LinkedIn, extracts job descriptions, processes resume files (PDF, DOCX, TXT), and uses AI (via OpenAI) to analyze matches, highlighting strengths, gaps, suggestions, and a match score. The tool leverages natural language processing for insightful feedback beyond simple keyword matching.

This project was developed as part of the HCI 584 (Human-Computer Interaction) course. Initially a CLI prototype (Version 1), it has now evolved to include a public-facing web app using Streamlit (Version 2), deployed at https://resumesyncbeta.streamlit.app/, making it accessible via a browser. The repository is structured for clarity, with entry points in `main.py` for CLI and `app.py` for the Streamlit GUI. Recent updates, including several commits on December 12, 2025, implemented the GUI, improved error handling, added deployment configurations (e.g., secrets template for Streamlit), updated output formatting, enhanced the resume match scoreboard display, and polished the overall app.

**Project Cleanup Notes**: Per Lecture 10, the project has been cleaned: Files use descriptive names (e.g., `job_spy.py` for scraping, `resume_analyzer.py` for AI), and entry points are obvious. No pip-installable package was created.

**In-Code Documentation**: All modules, classes, and functions use consistent Google-style docstrings. Inline # comments explain complex logic, and # TODO comments flag areas like adding retry logic for scraping. # GOTCHA notes highlight potential issues, e.g., LinkedIn HTML changes.

## Condensed Version of Final Planning Specs

The initial project specs (detailed in `Docs/Resume Sync_Project Sync_Update_30Oct.pdf`) outlined a multi-version rollout:

- **Version 1 (CLI Prototype - Implemented):**
  - Scrape real job postings from LinkedIn using JobSpy (limited to 5 results to avoid rate limits).
  - Display jobs in a picklist and allow user selection.
  - Fetch full job description from selected LinkedIn URL (using web scraping as a fallback for public pages).
  - Extract text from uploaded resume (PDF, DOCX, or TXT).
  - Use OpenAI API to compare resume with job description, outputting match score, matched/missing skills, and summary.
  - Handle errors gracefully, with a mock mode for AI analysis if no API key is provided.

- **Version 2 (Enhanced Web Interface - Implemented):**
  - Streamlit app with drag-and-drop resume upload and form inputs for job search.
  - Visual dashboards for analysis results (e.g., skill match visualizations, scoreboard display).
  - Bulk resume analysis and history tracking (stored locally or in session).
  - Export results to PDF reports.
  - Integrated job scraping and AI analysis in the backend.

- **Changes from Initial Specs:**
  - Aborted scraping from other sites (e.g., Indeed, Glassdoor, ZipRecruiter) due to access restrictions and lack of public APIs/links.
  - Merged resume extraction into the AI comparison flow for simplicity.
  - Added support for direct LinkedIn URL pasting as an alternative to searching.
  - Simplified match output to structured formats (terminal for CLI, dashboards for GUI).
  - Deferred advanced features like optimization dashboards to future updates; basic visuals and scoreboard implemented in Version 2.

- **Implemented Components:**
  - Job Scraping: Fully functional with JobSpy.
  - Resume Processing: Handles PDF/DOCX/TXT.
  - AI Analysis: Integrated with OpenAI (gpt-4o-mini); mock fallback.
  - Interfaces: CLI menu-driven; Streamlit GUI with interactive elements.

All core workflows from the specs are implemented across Versions 1 and 2, with refinements for robustness (e.g., user agent rotation for scraping, JSON normalization for AI outputs). Updates as of December 12, 2025, include app name simplification, dev container addition, job description formatting improvements, scoreboard display enhancements, error handling in app.py, and Streamlit deployment preparations.

## Install/Deployment/Admin Issues

Assuming the developer has read the user's guide (README.md) and installed the project via `pip install -r requirements.txt`, here are additional dev-specific notes:

- **Environment Setup:**
  - Create a `.env` file in the root with `OPENAI_API_KEY=your_key_here` for live AI analysis. Without it, defaults to mock mode (set `USE_MOCK=true` to force).
  - `requirements.txt` includes `jobspy`, `beautifulsoup4`, `PyPDF2`, `python-docx`, `openai`, `python-dotenv`, `requests`, `streamlit`, and others for GUI (e.g., `pandas` for data handling, `reportlab` for PDF exports).
  - Run in a virtual environment with Python 3.8+. For GUI, install Streamlit extras if needed.
  - Added `.devcontainer` folder for development environments (e.g., VS Code Remote Containers).

- **Running the App:**
  - CLI: `python main.py`.
  - GUI: `streamlit run app.py` (launches at http://localhost:8501).
  - No database required; history uses Streamlit session state.

- **Deployment Notes:**
  - The app is now public-facing: Deployed to Streamlit Cloud at https://resumesyncbeta.streamlit.app/. For your own deployment, use Streamlit Cloud via GitHub integration or platforms like Heroku/Render. Update `requirements.txt` and add a `Procfile` for web: `streamlit run --server.port $PORT app.py`.
  - Use `.streamlit/secrets.toml` (template added in commits) for secrets like API keys in deployment.
  - For production: Monitor OpenAI costs (~$0.01–0.05 per analysis). Use environment variables for secrets.
  - Configure proxies/VPN if LinkedIn blocks during scraping.
  - Admin: No special privileges; but for public deployment, add rate limiting or CAPTCHA if usage grows.

- **Watchouts:**
  - LinkedIn scraping may fail for private pages—placeholder used.
  - API limits: JobSpy ~50 results; OpenAI token limits (inputs truncated).
  - GUI-specific: File uploads limited by Streamlit (adjust in config if needed).

## (End) User Interaction and Flow Through Your Code (Walkthrough)

The user experience now includes both CLI and GUI options, with the GUI providing a more intuitive, visual interface. Here's a brief recap of the flows, followed by code walkthroughs.

### User Interaction Flow (CLI - Version 1)

1. Launch via `python main.py`.
2. Menu: Browse jobs, paste URL, or exit.
3. Browse: Enter title (e.g., "UX Designer") and location. Fetches 5 jobs, displays numbered list.
4. Select job: Prints description.
5. Analyze: Enter resume path. Prints results (score, skills, summary).
6. Repeat/exit. User-friendly error messages.

### User Interaction Flow (GUI - Version 2)

1. Access via https://resumesyncbeta.streamlit.app/ or local run.
2. Sidebar: Input job title/location or paste URL.
3. Main page: Upload resume (drag-and-drop), click "Analyze".
4. Results: Dashboard with match score, lists of strengths/gaps, recommendations, and visuals (e.g., bar charts for skill matches, improved scoreboard).
5. Additional: View history, export PDF, bulk upload for multiple resumes.
6. UX: Responsive design, loading spinners for scraping/AI, error messages for issues.

UX emphasizes minimal inputs, clear visuals, and actionable insights in both modes.

For visuals, here's an example screenshot of the Streamlit GUI homepage:

![Streamlit GUI Homepage](docs/images/gui_homepage.png) 

Resume analysis dashboard:

![Analysis Dashboard](docs/images/analysis_dashboard.png) 

### Code Flow Walkthrough

Code is modularized. Assume viewing code while reading.

- **CLI Entry (`main.py`):**
  - `main()`: CLI loop, calls `search_flow()` (prompts, `job_spy.get_jobs()`, `job_spy.print_picklist()`, `job_detail.fetch_job_description()`, `offer_resume_analysis()`).
  - `offer_resume_analysis()`: Resume path, `resume_reader.read_resume_text()`, `resume_analyzer.analyze_resume_match()`, normalize, print.

- **GUI Entry (`app.py`):**
  - Streamlit setup: `st.title()`, sidebar inputs for search/URL/upload.
  - On submit: Calls scraping modules (`job_spy`, `job_detail`), resume processing, AI analysis.
  - Displays results with `st.write()`, `st.dataframe()` for tables, `st.bar_chart()` for visuals, improved scoreboard.
  - History: Uses `st.session_state` to store analyses.
  - Export: Generates PDF with `reportlab` or Streamlit's download button.
  - Error handling: Enhanced try-except blocks for robustness.

- **Shared Modules:**
  - `job_spy.py`: `get_jobs()` uses `jobspy.scrape_jobs()`.
  - `job_detail.py`: `fetch_job_description()` with requests/BeautifulSoup, headers from `user_agents.py`, updated formatting.
  - `resume_reader.py`: `read_resume_text()` handles file types.
  - `resume_analyzer.py`: `analyze_resume_match()` OpenAI client, prompt building, JSON parsing, mock mode, recent improvements.

Overall flow (GUI): User inputs → Scraping → Resume read → AI → Dashboard render in `app.py`.
Hierarchies: No deep inheritance; Streamlit pages as functions.

For visuals, a flow diagram:

```
User Inputs (app.py) → get_jobs (job_spy.py) → fetch_job_description (job_detail.py) → read_resume_text (resume_reader.py) → analyze_resume_match (resume_analyzer.py) → Render Dashboard (app.py)
```

### Module Overview Table

| Module              | Key Functions/Classes              | Purpose                          |
|---------------------|------------------------------------|----------------------------------|
| `app.py`           | Streamlit setup, submit handlers   | GUI entry and rendering         |
| `main.py`          | `main()`, `search_flow()`         | CLI entry and loops             |
| `job_spy.py`       | `get_jobs()`                      | Job scraping with JobSpy        |
| `job_detail.py`    | `fetch_job_description()`         | Description extraction          |
| `resume_reader.py` | `read_resume_text()`              | Resume file processing          |
| `resume_analyzer.py` | `analyze_resume_match()`        | AI analysis with OpenAI         |

## Known Issues

### Minor (Non-Breaking)

- Job descriptions incomplete if LinkedIn HTML changes—update selectors in `job_detail.py`.
- Mock mode fixed data; toggle in `.env`.
- GUI: Long texts may overflow dashboards—add scrolling.
- Recent commits fixed minor UI bugs, but test cross-browser.

### Major (Potential Breaking)

- Scraping blocks: No auto-retry; workaround VPN. Fix: Backoff in `requests`.
- OpenAI errors: Caught, app continues. Fix: Retry in `resume_analyzer.py`.
- File formats: Errors for unsupported—expand `resume_reader.py`.
- Deployment: Streamlit Cloud may have file size limits for uploads. Recent bug fixes addressed analyzer issues.

## Computational Inefficiencies (Optional)

- Scraping synchronous—slow for larger results. Use async for scale.
- AI calls per-analysis; batch for bulk mode.
- Pure Python fine for small; local LLMs (Hugging Face) for cost savings.
- Streamlit redraws on interactions—optimize with caching (`@st.cache_data`).

## Future Work

- Advanced visuals: Full optimization dashboard with resume editing suggestions.
- Expand scraping: Official APIs if available.
- Add user auth for history persistence (e.g., SQLite/Cloud DB).
- Mobile responsiveness in GUI.
- Inefficiencies: Cache descriptions, GPU for local models.

## Ongoing Deployment/Development

With the public-facing app, expect ongoing use. For continuity:

- Unit tests (pytest) for core functions to handle site changes.
- Extensibility: Subclass readers/analyzers for new formats/models.
- Infrastructure: CI/CD via GitHub Actions for deployments.
- Changes: Semantic versioning; PR templates. Monitor logs for issues. For the deployed app, use Streamlit Cloud monitoring; implement GitHub Actions for CI/CD to auto-deploy on main branch pushes.
