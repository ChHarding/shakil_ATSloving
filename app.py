import json
import streamlit as st
from PyPDF2 import PdfReader

# Your project modules
from job_spy import get_jobs          # must exist in job_spy.py
from job_detail import fetch_job_description  # must exist in job_detail.py
from resume_analyzer import analyze_resume_match  # must exist in resume_analyzer.py


# =========================
# HELPER: EXTRACT RESUME TEXT
# =========================

def extract_resume_text(uploaded_file) -> str:
    """Extract plain text from a PDF uploaded via Streamlit."""
    try:
        reader = PdfReader(uploaded_file)
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        text_all = "\n".join(pages_text).strip()
        return text_all
    except Exception as e:
        return f"[ERROR extracting resume text: {e}]"


# =========================
# HELPER: SHOW MATCH RESULT
# =========================

def show_match_result(result):
    """
    Render the OpenAI analysis nicely.

    Expected dict format:
    {
      "match_score": int 0-100,
      "matched_skills": [..],
      "missing_skills": [..],
      "summary": "..."
    }

    If it's a plain string, just show it.
    """
    # If OpenAI returned just text or an error string
    if isinstance(result, str):
        st.text_area("Analysis", result, height=250)
        return

    if "error" in result:
        st.error(f"OpenAI error: {result['error']}")
        return

    score = result.get("match_score")
    matched = result.get("matched_skills", [])
    missing = result.get("missing_skills", [])
    summary = result.get("summary", "")

    if score is not None:
        st.subheader("📊 Match Score")
        st.metric("Match", f"{score} / 100")
        s = min(max(score, 0), 100)  # clamp 0–100
        st.progress(s / 100.0)

    st.subheader("✅ Matched Skills")
    if matched:
        st.write(", ".join(matched))
    else:
        st.write("_No clearly matched skills parsed._")

    st.subheader("⚠️ Missing or Weaker Skills")
    if missing:
        st.write(", ".join(missing))
    else:
        st.write("_No obvious missing skills identified._")

    st.subheader("💡 Summary & Suggestions")
    st.write(summary or "_No summary returned._")


# =========================
# STREAMLIT PAGE CONFIG
# =========================

st.set_page_config(
    page_title="ResumeSync",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 ResumeSync – Smart Resume–Job Match (Streamlit Web App)")
st.caption(
    "Search LinkedIn jobs or paste a LinkedIn URL, then upload your resume and get an AI-powered match report."
)

tab_search, tab_url = st.tabs(["🔎 Search LinkedIn Jobs", "🔗 Paste LinkedIn Job URL"])


# -------------------------------------------------------------------
# TAB 1: SEARCH LINKEDIN JOBS (via job_spy.get_jobs)
# -------------------------------------------------------------------
with tab_search:
    st.header("🔎 Search LinkedIn Jobs")

    # Initialize state for search_jd_text
    if "search_jd_text" not in st.session_state:
        st.session_state["search_jd_text"] = ""

    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Job title", value="UX Designer")
    with col2:
        location = st.text_input("Location", value="United States")

    num_results = st.slider("Number of jobs to fetch", 3, 10, 5)

    jobs_df = None

    if st.button("Search LinkedIn via JobSpy"):
        with st.spinner("Searching LinkedIn…"):
            try:
                # IMPORTANT: positional call to avoid keyword argument error
                jobs_df = get_jobs(role, location, num_results)
                st.session_state["jobs_df"] = jobs_df
            except Exception as e:
                st.error(f"Error fetching jobs: {e}")
                jobs_df = None

    # Reuse previous search results if they exist
    if "jobs_df" in st.session_state:
        jobs_df = st.session_state["jobs_df"]

    if jobs_df is not None and not jobs_df.empty:
        st.subheader("Results")
        display_cols = ["title", "company", "location", "job_url"]
        available_cols = [c for c in display_cols if c in jobs_df.columns]
        st.dataframe(jobs_df[available_cols])

        indices = list(jobs_df.index)
        chosen_idx = st.selectbox(
            "Select a job to view details",
            indices,
            format_func=lambda i: f"{i}: {jobs_df.iloc[i]['title']} @ {jobs_df.iloc[i]['company']}",
        )

        if st.button("Load Job Description for Selected Job"):
            row = jobs_df.iloc[chosen_idx]
            url = row.get("job_url", "")

            st.write(f"**Selected Job:** {row.get('title')} at {row.get('company')}")
            st.write(f"🔗 {url}")

            # Use description from JobSpy if present, otherwise fetch via job_detail.py
            if "description" in jobs_df.columns:
                desc = (row.get("description") or "").strip()
            else:
                desc = ""

            if not desc:
                with st.spinner("Fetching full job description from LinkedIn…"):
                    desc = fetch_job_description(url) or "[No description available – maybe private/login-only page.]"

            # Save to session_state BEFORE widget so no API exception
            st.session_state["search_jd_text"] = desc

            st.subheader("📄 Job Description")
            st.text_area(
                "Job Description Text",
                height=250,
                key="search_jd_text",
            )

    # Resume upload + analysis for SEARCH flow
    jd_text = st.session_state.get("search_jd_text", "")

    uploaded_resume_search = st.file_uploader(
        "Upload your resume (PDF) for the selected job",
        type=["pdf"],
        key="search_resume_uploader",
    )

    if uploaded_resume_search and jd_text and st.button("Analyze Match (Search Tab)"):
        with st.spinner("Extracting resume and analyzing match…"):
            resume_text = extract_resume_text(uploaded_resume_search)
            result = analyze_resume_match(resume_text, jd_text)
        show_match_result(result)
    elif uploaded_resume_search and not jd_text:
        st.info("Please load a job description first (above), then analyze.")


# -------------------------------------------------------------------
# TAB 2: PASTE LINKEDIN JOB URL
# -------------------------------------------------------------------
with tab_url:
    st.header("🔗 Paste a LinkedIn Job URL")

    # Initialize state for url_jd_text
    if "url_jd_text" not in st.session_state:
        st.session_state["url_jd_text"] = ""

    url = st.text_input("LinkedIn Job URL", key="url_input")

    if st.button("Fetch Job Description from URL"):
        if not url.strip():
            st.error("Please paste a LinkedIn job URL.")
        else:
            with st.spinner("Fetching job description from LinkedIn…"):
                desc = fetch_job_description(url) or "[No description available – maybe private/login-only page.]"

            # Save to session_state BEFORE widget so no API exception
            st.session_state["url_jd_text"] = desc

            st.subheader("📄 Job Description")
            st.text_area(
                "Job Description Text",
                height=250,
                key="url_jd_text",
            )

    jd_text_url = st.session_state.get("url_jd_text", "")

    uploaded_resume_url = st.file_uploader(
        "Upload your resume (PDF) for this job",
        type=["pdf"],
        key="url_resume_uploader",
    )

    if uploaded_resume_url and jd_text_url and st.button("Analyze Match (URL Tab)"):
        with st.spinner("Extracting resume and analyzing match…"):
            resume_text = extract_resume_text(uploaded_resume_url)
            result = analyze_resume_match(resume_text, jd_text_url)
        show_match_result(result)
    elif uploaded_resume_url and not jd_text_url:
        st.info("Please fetch a job description first, then analyze.")
