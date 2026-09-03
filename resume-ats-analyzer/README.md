# 📄 Resume ATS Analyzer

An AI-powered Streamlit application that analyzes a resume against a target job description and provides a **heuristic ATS score**, keyword matching, strengths, improvement suggestions, ATS risks, and resume bullet rewrites using **Google Gemini Flash**.

> **Note:** The ATS score is an AI-generated estimate and is not an official score from any ATS vendor.

## ✨ Features

* Upload resumes in **PDF, DOCX, or TXT** format
* Paste a target **Job Description**
* Extract resume text automatically
* Generate an ATS score out of **100**
* Score breakdown by:

  * Keyword Match
  * Experience Relevance
  * ATS Structure
  * Role Alignment
  * Education & Certifications
  * Impact & Action Language
* Identify matched and missing keywords
* Highlight resume strengths
* Provide prioritized improvements
* Detect potential ATS formatting risks
* Generate factual, ATS-friendly bullet rewrites
* Download analysis as JSON
* Uses evidence-based analysis to reduce fabricated metrics and skills

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini Flash**
* **Google GenAI SDK**
* **PyPDF**
* **python-docx**

## 📁 Project Structure

```text
resume-ats-analyzer/
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your Gemini API key:

```text
GEMINI_API_KEY=your_api_key
```

For Streamlit Cloud, add `GEMINI_API_KEY` under:

**App → Settings → Secrets**

Run locally:

```bash
streamlit run app.py
```

## 🚀 How to Use

1. Upload your resume.
2. Paste the complete target job description.
3. Click **Analyze Resume**.
4. Review the ATS score and recommendations.
5. Download the analysis as JSON if required.

## 🔐 Privacy

Resume text is sent to the **Gemini API** for analysis. Do not upload documents you are not authorized to share.

## 📌 Disclaimer

This application provides an **AI-generated heuristic ATS estimate** for resume improvement. It does not represent the scoring system of any specific Applicant Tracking System.

