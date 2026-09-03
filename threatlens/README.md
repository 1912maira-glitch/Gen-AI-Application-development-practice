# 🛡️ ThreatLens

### IP, Domain & URL Safety Intelligence

ThreatLens is a Streamlit-based cybersecurity application that analyzes **IP addresses, domains, and URLs** using threat intelligence from **VirusTotal** and **WHOIS/RDAP**, with **Google Gemini** providing an AI-assisted security assessment.

The application combines multiple sources into a simple security report containing a **verdict, confidence score, key findings, recommendation, and source evidence**.

---

## ✨ Features

- 🔍 Analyze **IP addresses, domains, and URLs**
- 🦠 VirusTotal threat intelligence lookup
- 🌐 WHOIS/RDAP registration and network information
- 🤖 Google Gemini AI-assisted security analysis
- 📊 Security verdict and confidence score
- 📝 Summary, key findings, and recommendations
- 🎓 Beginner, Intermediate, and Advanced knowledge levels
- ⚠️ Input validation and error handling
- 🔐 API keys managed through Streamlit Secrets
- 📂 Expandable source evidence for transparency

---

## 🔄 How It Works

```text
User Input
    ↓
Input Validation
    ↓
VirusTotal + WHOIS/RDAP
    ↓
Evidence Collection
    ↓
Google Gemini
    ↓
Security Assessment
    ↓
Verdict + Confidence + Findings
```

ThreatLens does **not** directly execute or visit submitted URLs. It uses external intelligence services to analyze the supplied indicators.

---

## 📊 Security Verdicts

| Verdict | Meaning |
|---|---|
| 🟢 SAFE | No significant malicious indicators found in the available evidence |
| 🟡 SUSPICIOUS | Some indicators require caution or further investigation |
| 🔴 MALICIOUS | Strong evidence indicates malicious activity |
| ⚪ UNKNOWN | Insufficient evidence for a reliable assessment |

> A `SAFE` result does not guarantee that a target is completely safe, and `UNKNOWN` does not mean malicious.

---

## 🎓 Knowledge Levels

ThreatLens provides three explanation levels:

- **Beginner** — Simple, easy-to-understand security explanations
- **Intermediate** — More technical analysis of security indicators
- **Advanced** — Analyst-oriented interpretation of available evidence

---

## 🌐 Intelligence Sources

### VirusTotal

Used for reputation and threat-detection information for supported IP addresses, domains, and URLs.

### WHOIS/RDAP

Used to obtain available registration and network information such as:

- Domain registration details
- ASN information
- Network/registry information
- Domain status

A failed or unavailable WHOIS/RDAP lookup does **not** automatically indicate that a target is malicious.

---

## 🤖 AI Analysis

Google Gemini interprets the collected intelligence and generates:

- **Summary**
- **Key Findings**
- **Recommendation**
- **Verdict**
- **Confidence Score**

The AI assessment is based on the evidence collected by ThreatLens and is intended to assist investigation rather than replace human judgment.

---

## 📁 Project Structure

```text
threatlens/
│
├── app.py
├── sources.py
├── requirements.txt
├── README.md
└── .gitignore
```

### `app.py`

Main Streamlit application containing:

- User interface
- Input validation
- Source orchestration
- Gemini analysis
- Result display

### `sources.py`

Handles:

- VirusTotal integration
- WHOIS/RDAP integration
- Source registry
- Source result processing

### `requirements.txt`

Contains the Python dependencies required to run the application.

---

## 🛠️ Technology Stack

- **Python**
- **Streamlit**
- **VirusTotal API**
- **WHOIS/RDAP**
- **Google Gemini API**

---

## 🔑 API Configuration

ThreatLens requires:

```text
VIRUSTOTAL_API_KEY
GEMINI_API_KEY
```

### Local Development

Create:

```text
.streamlit/secrets.toml
```

and add:

```toml
VIRUSTOTAL_API_KEY = "your_virustotal_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
```

**Never commit API keys to GitHub.**

Add this to `.gitignore`:

```text
.streamlit/secrets.toml
```

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/threatlens.git
cd threatlens
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create:

```text
.streamlit/secrets.toml
```

with your API keys.

### 5. Start ThreatLens

```bash
streamlit run app.py
```

---

## ☁️ Streamlit Deployment

ThreatLens can be deployed directly from GitHub using Streamlit Community Cloud.

### Deployment Steps

1. Push the project to GitHub.
2. Create a new Streamlit application.
3. Select your `threatlens` repository.
4. Select the `main` branch.
5. Set the main file to:

```text
app.py
```

6. Add the following secrets in Streamlit:

```toml
VIRUSTOTAL_API_KEY = "your_virustotal_api_key"
GEMINI_API_KEY = "your_gemini_api_key"
```

7. Deploy the application.

---

## 🧪 Example Inputs

### IP Address

```text
8.8.8.8
```

### Domain

```text
example.com
```

### URL

```text
https://example.com
```

You can also test invalid inputs to verify the application's validation and error handling.

---

## 🔐 Security Considerations

ThreatLens is designed as a **defensive threat-intelligence and analysis tool**.

It:

- Does not execute malware
- Does not exploit systems
- Does not perform penetration testing
- Does not automatically block or quarantine targets
- Does not require API keys to be stored in source code
- Treats external intelligence as untrusted evidence

Always review the underlying source evidence before making important security decisions.

---

## ⚠️ Limitations

ThreatLens depends on external services, so results may be affected by:

- API availability
- Rate limits
- Network errors
- Missing intelligence
- Incomplete WHOIS/RDAP records
- False positives or false negatives
- AI interpretation limitations

The application should be treated as an **investigation aid**, not an absolute security decision engine.

---

## 🎯 Use Cases

ThreatLens can be used for:

- Cybersecurity education
- Threat-intelligence research
- Initial IOC investigation
- Suspicious IP/domain/URL analysis
- Security demonstrations
- AI-assisted defensive analysis

---

## ⚖️ Disclaimer

ThreatLens provides information and AI-assisted analysis based on available external intelligence.

A `SAFE`, `SUSPICIOUS`, `MALICIOUS`, or `UNKNOWN` result should not be considered an absolute determination of the target's security status.

Always verify important findings using additional trusted security tools and sources.

---

## 📄 License

No open-source license is currently specified for this project.

If you plan to distribute or allow others to modify the project, add an appropriate license such as MIT or Apache-2.0.

---

## 👨‍💻 ThreatLens

**ThreatLens — IP, Domain & URL Safety Intelligence**

Built with:

```text
Python • Streamlit • VirusTotal • WHOIS/RDAP • Google Gemini
```
