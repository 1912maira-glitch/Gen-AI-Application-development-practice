import io
import json
import os
import re
from typing import Any, Dict

import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader
from docx import Document

MODEL_NAME = "gemini-2.5-flash"

st.set_page_config(page_title="Resume ATS Analyzer", page_icon="📄", layout="wide")


def get_api_key() -> str:
    """Read the Gemini API key from Streamlit secrets or the environment."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "").strip()


def extract_text(uploaded_file) -> str:
    """Extract text from PDF, DOCX, or TXT uploads."""
    suffix = uploaded_file.name.lower().rsplit(".", 1)[-1]
    data = uploaded_file.getvalue()

    if suffix == "pdf":
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if suffix == "docx":
        doc = Document(io.BytesIO(data))
        parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                parts.append(paragraph.text)
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text.strip() for cell in row.cells))
        return "\n".join(parts)

    if suffix == "txt":
        return data.decode("utf-8", errors="ignore")

    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")


def clean_json(text: str) -> Dict[str, Any]:
    """Parse JSON even if the model accidentally wraps it in a markdown fence."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def analyze_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to Streamlit Secrets "
            "or set it as an environment variable."
        )

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are an expert ATS resume evaluator and career coach.

Analyze the resume against the job description. The ATS score is a
HEURISTIC estimate, not a score produced by a real ATS vendor.

Scoring rubric (total 100):
- Keyword/skill match: 35
- Relevant experience and achievements: 25
- ATS-friendly structure/format signals: 15
- Role/title alignment: 10
- Education/certification alignment: 5
- Measurable impact and strong action language: 10

Important:
- Do not invent experience, skills, employers, education, or metrics.
- Penalize missing important job-description keywords, but distinguish
  between a genuinely missing skill and a skill that is simply phrased differently.
- Do not reward keyword stuffing.
- Flag possible ATS parsing risks such as tables, columns, graphics, headers/footers,
  unusual symbols, or missing standard section headings only when supported by the text.
- Give actionable improvements prioritized by impact.
- Keep feedback concise and specific.

Return ONLY valid JSON matching this exact schema:
{{
  "ats_score": 0,
  "score_breakdown": {{
    "keyword_match": 0,
    "experience_relevance": 0,
    "ats_structure": 0,
    "role_alignment": 0,
    "education_certifications": 0,
    "impact_action_language": 0
  }},
  "summary": "string",
  "matched_keywords": ["string"],
  "missing_keywords": ["string"],
  "strengths": ["string"],
  "improvements": [
    {{
      "priority": "High|Medium|Low",
      "issue": "string",
      "recommendation": "string",
      "example": "string"
    }}
  ],
  "ats_format_risks": ["string"],
  "rewrites": [
    {{
      "original": "string",
      "improved": "string"
    }}
  ]
}}

Resume:
---BEGIN RESUME---
{resume_text[:50000]}
---END RESUME---

Job description:
---BEGIN JOB DESCRIPTION---
{job_description[:20000]}
---END JOB DESCRIPTION---
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    result = clean_json(response.text)

    # Defensive validation so a malformed model response does not break the UI.
    score = int(result.get("ats_score", 0))
    result["ats_score"] = max(0, min(100, score))

    required_lists = [
        "matched_keywords",
        "missing_keywords",
        "strengths",
        "improvements",
        "ats_format_risks",
        "rewrites",
    ]
    for key in required_lists:
        if not isinstance(result.get(key), list):
            result[key] = []

    return result


def display_score(score: int) -> None:
    st.metric("Estimated ATS Score", f"{score}/100")
    st.progress(score / 100)


def main() -> None:
    st.title("📄 Resume ATS Analyzer")
    st.caption(
        "Upload a resume and paste a target job description to get an "
        "AI-powered, heuristic ATS score and targeted improvements."
    )

    with st.sidebar:
        st.header("How it works")
        st.write(
            "1. Upload your resume.\n"
            "2. Paste the target job description.\n"
            "3. Gemini compares them using a transparent scoring rubric.\n"
            "4. Review the gaps and suggested rewrites."
        )
        st.info(
            "Privacy note: the resume text is sent to the Gemini API for analysis. "
            "Do not upload documents you are not authorized to share."
        )

    uploaded_file = st.file_uploader(
        "Upload resume",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX, TXT.",
        max_upload_size=10,
    )

    job_description = st.text_area(
        "Paste the target job description",
        height=260,
        placeholder="Paste the complete job description here...",
    )

    if uploaded_file:
        try:
            resume_text = extract_text(uploaded_file)
            if not resume_text.strip():
                st.error(
                    "No text could be extracted. If this is a scanned PDF, "
                    "use an OCR-enabled PDF or upload a DOCX/TXT version."
                )
                return
            st.success(f"Extracted approximately {len(resume_text):,} characters.")
            with st.expander("Preview extracted resume text"):
                st.text(resume_text[:5000])
        except Exception as exc:
            st.error(f"Could not read the resume: {exc}")
            return
    else:
        resume_text = ""

    analyze_clicked = st.button(
        "Analyze Resume",
        type="primary",
        use_container_width=True,
        disabled=not uploaded_file or not job_description.strip(),
    )

    if analyze_clicked:
        with st.spinner("Analyzing your resume with Gemini..."):
            try:
                result = analyze_resume(resume_text, job_description.strip())
                st.session_state["analysis"] = result
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")
                st.exception(exc)

    result = st.session_state.get("analysis")
    if not result:
        return

    st.divider()
    display_score(result["ats_score"])

    st.subheader("Summary")
    st.write(result.get("summary", "No summary returned."))

    st.subheader("Score breakdown")
    breakdown = result.get("score_breakdown", {})
    cols = st.columns(3)
    labels = [
        ("Keyword match", "keyword_match"),
        ("Experience relevance", "experience_relevance"),
        ("ATS structure", "ats_structure"),
        ("Role alignment", "role_alignment"),
        ("Education/certifications", "education_certifications"),
        ("Impact/action language", "impact_action_language"),
    ]
    for index, (label, key) in enumerate(labels):
        with cols[index % 3]:
            st.metric(label, breakdown.get(key, 0))

    left, right = st.columns(2)
    with left:
        st.subheader("✅ Matched keywords")
        st.write(", ".join(result.get("matched_keywords", [])) or "None identified.")
    with right:
        st.subheader("⚠️ Missing keywords")
        st.write(", ".join(result.get("missing_keywords", [])) or "None identified.")

    st.subheader("Strengths")
    for item in result.get("strengths", []):
        st.markdown(f"- {item}")

    st.subheader("Priority improvements")
    for item in result.get("improvements", []):
        priority = item.get("priority", "Medium")
        st.markdown(
            f"**{priority}: {item.get('issue', 'Improvement')}**  \n"
            f"{item.get('recommendation', '')}"
        )
        if item.get("example"):
            st.caption(f"Example: {item['example']}")

    st.subheader("ATS format risks")
    risks = result.get("ats_format_risks", [])
    if risks:
        for risk in risks:
            st.markdown(f"- {risk}")
    else:
        st.write("No major ATS format risks were identified from the extracted text.")

    rewrites = result.get("rewrites", [])
    if rewrites:
        st.subheader("Suggested bullet rewrites")
        for item in rewrites:
            st.markdown(f"**Original:** {item.get('original', '')}")
            st.markdown(f"**Improved:** {item.get('improved', '')}")
            st.divider()

    st.download_button(
        "Download analysis as JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="resume_ats_analysis.json",
        mime="application/json",
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
