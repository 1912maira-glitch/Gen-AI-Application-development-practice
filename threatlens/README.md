# 🛡️ ThreatLens

### IP, Domain & URL Safety Intelligence

ThreatLens is a lightweight cybersecurity intelligence and security-analysis application built with **Python** and **Streamlit**.

The application allows users to analyze an **IP address, domain, or URL** using intelligence collected from **VirusTotal** and **WHOIS/RDAP** services. The collected evidence is then passed to **Google Gemini** for an evidence-based security assessment.

ThreatLens provides a clear security verdict, confidence score, AI-generated summary, key findings, recommendations, and access to the underlying source evidence.

---

# 🔎 Overview

ThreatLens is designed to provide a simple interface for performing initial security intelligence checks on potentially suspicious infrastructure.

Instead of requiring a user to manually query multiple intelligence services, ThreatLens combines the available evidence into a single analysis workflow.

The application supports:

- IP address analysis
- IPv4 analysis
- IPv6 analysis
- Domain analysis
- URL analysis
- VirusTotal intelligence
- WHOIS/RDAP information
- AI-assisted evidence interpretation
- Beginner-friendly explanations
- Intermediate-level explanations
- Advanced analyst-oriented explanations
- Security verdicts
- Confidence scores
- Key findings
- Recommendations
- Source evidence inspection
- Graceful handling of API failures

ThreatLens is intended to be an **intelligence and investigation aid** rather than an automated offensive security platform.

---

# ✨ Key Features

## 🎯 Multiple Target Types

Users can analyze:

- IPv4 addresses
- IPv6 addresses
- Domain names
- HTTP URLs
- HTTPS URLs

---

## 🧠 Multiple Knowledge Levels

ThreatLens supports:

- Beginner
- Intermediate
- Advanced

The selected knowledge level influences how the AI explains the collected evidence.

---

## 🔍 Multiple Intelligence Sources

ThreatLens currently uses:

1. **VirusTotal**
2. **WHOIS/RDAP**

Each source is queried independently.

---

## 🤖 AI-Assisted Analysis

Google Gemini analyzes the collected intelligence and produces:

- Security verdict
- Confidence score
- Summary
- Key findings
- Recommendation

The AI is instructed to base its assessment on the evidence supplied by the application.

---

## 📊 Evidence-Based Results

ThreatLens does not only display an AI conclusion.

The underlying source evidence is also displayed so users can manually review the information used during the assessment.

---

## ⚠️ Graceful Failure Handling

The application is designed to continue operating even when an individual intelligence source or AI service is unavailable.

For example:

```text
VirusTotal unavailable
        ↓
WHOIS/RDAP may still work
        ↓
Source evidence remains available
```

Similarly:

```text
Gemini unavailable
        ↓
Source evidence remains available
        ↓
AI analysis is marked unavailable
```

---

# 🔄 How ThreatLens Works

The overall architecture is:

```text
                 USER
                  │
                  ▼
        ┌─────────────────────┐
        │  Streamlit Web UI   │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Input Validation    │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Target Normalization│
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │  Source Registry    │
        └──────────┬──────────┘
                   │
          ┌────────┴────────┐
          ▼                 ▼
 ┌────────────────┐  ┌────────────────┐
 │   VirusTotal   │  │  WHOIS / RDAP  │
 └────────┬───────┘  └────────┬───────┘
          │                   │
          └─────────┬─────────┘
                    ▼
          ┌───────────────────┐
          │ Evidence Aggregate│
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │   Google Gemini   │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Security Verdict  │
          │ Confidence        │
          │ Findings          │
          │ Recommendation    │
          └─────────┬─────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Source Evidence   │
          │ + AI Assessment   │
          └───────────────────┘
```

---

# 🔁 Application Workflow

When a user clicks **Analyze**, ThreatLens follows this sequence:

```text
1. User selects target type
              ↓
2. User selects knowledge level
              ↓
3. User enters target
              ↓
4. Target is validated
              ↓
5. Target is normalized
              ↓
6. Registered intelligence sources are executed
              ↓
7. VirusTotal lookup
              ↓
8. WHOIS/RDAP lookup
              ↓
9. Source results are normalized
              ↓
10. Evidence is aggregated
              ↓
11. Gemini prompt is constructed
              ↓
12. Gemini analyzes the evidence
              ↓
13. Structured AI response is parsed
              ↓
14. Verdict and confidence are displayed
              ↓
15. AI Security Assessment is displayed
              ↓
16. Source Evidence is displayed
```

---

# 🎯 Supported Target Types

ThreatLens supports three primary target types.

---

## 1. IP Address

Both IPv4 and IPv6 addresses are supported.

### IPv4 Example

```text
8.8.8.8
```

### IPv6 Example

```text
2001:4860:4860::8888
```

IP addresses are validated before any external intelligence lookup occurs.

---

## 2. Domain

A domain can be entered directly.

Example:

```text
example.com
```

The domain is normalized before the relevant intelligence providers are queried.

---

## 3. URL

HTTP and HTTPS URLs are supported.

Example:

```text
https://example.com
```

Another example:

```text
https://example.com/login
```

For domain intelligence, the hostname can be extracted from the URL.

---

# 🎓 Knowledge Levels

ThreatLens allows the user to choose how the security assessment should be explained.

---

## 🟢 Beginner

The Beginner level is designed for users who may have limited cybersecurity knowledge.

The assessment focuses on:

- Simple explanations
- Avoiding unnecessary technical jargon
- Explaining what the evidence means
- Explaining why something may be considered safe or suspicious
- Simple recommendations

Example style:

```text
The available security information does not show
strong signs of malicious activity. However, this
does not guarantee that the target is completely safe.
```

---

## 🟡 Intermediate

The Intermediate level is intended for users with basic cybersecurity knowledge.

The assessment can discuss:

- Reputation
- Detection results
- Registration information
- Network information
- Security indicators
- Evidence inconsistencies
- Investigation recommendations

---

## 🔴 Advanced

The Advanced level is intended for security analysts and technically experienced users.

The assessment focuses more heavily on:

- Indicators
- Reputation signals
- Detection ratios
- ASN information
- Registration information
- Infrastructure characteristics
- Confidence
- Uncertainty
- Investigation considerations

---

# 🌐 Threat Intelligence Sources

ThreatLens currently uses two intelligence sources.

```text
┌─────────────────────────┐
│      VirusTotal         │
│ Reputation / Detection  │
└────────────┬────────────┘
             │
             ▼
      ThreatLens Evidence
             ▲
             │
┌────────────┴────────────┐
│      WHOIS / RDAP       │
│ Registration / Network  │
└─────────────────────────┘
```

---

# 🦠 VirusTotal Integration

VirusTotal is used as a threat-intelligence and reputation source.

Depending on the target type, ThreatLens can use VirusTotal information for:

- IP addresses
- Domains
- URLs

The application extracts relevant information and places it into a normalized source-result structure.

VirusTotal results may contain information such as:

- Malicious detections
- Suspicious detections
- Harmless/undetected results
- Reputation-related information
- Other available intelligence

The exact information available depends on the target and VirusTotal's response.

---

# 🌍 WHOIS/RDAP Integration

WHOIS/RDAP provides registration and network context.

For domains, available information can include:

- Domain name
- TLD
- SLD
- Registration information
- Domain status
- WHOIS data

For IP addresses, available information can include:

- ASN
- ASN description
- ASN country
- ASN registry
- Network information
- Registration objects

---

## Important WHOIS/RDAP Behavior

A WHOIS/RDAP lookup can fail even when the target itself is valid.

For example:

```text
Lookup failed or unsupported
```

does not automatically mean:

```text
MALICIOUS
```

Possible reasons include:

- Missing records
- Unsupported lookup type
- Provider limitations
- Privacy-protected registration
- Network errors
- API/provider availability
- Parser limitations

ThreatLens treats missing source information as a limitation rather than automatically treating it as malicious evidence.

---

# 🤖 Google Gemini AI Analysis

ThreatLens uses Google Gemini as an **evidence interpretation layer**.

Gemini does not directly replace the intelligence sources.

The application first collects evidence:

```text
VirusTotal
    +
WHOIS/RDAP
```

and then sends the normalized evidence to Gemini.

Conceptually:

```text
Target
  ↓
Threat Intelligence
  ↓
Normalized Evidence
  ↓
Gemini
  ↓
Security Assessment
```

---

# 🧠 Evidence-Based AI

The Gemini analysis is designed to be grounded in the information collected by ThreatLens.

The AI is instructed to:

- Use the supplied evidence
- Avoid inventing information
- Acknowledge missing evidence
- Explain uncertainty
- Produce a structured response
- Adjust the explanation according to the selected knowledge level

The AI should not invent:

- VirusTotal detections
- WHOIS information
- ASN ownership
- Malware families
- Threat actors
- Geographic attribution
- Dates
- Registrars
- Reputation information

If evidence is unavailable, the assessment should acknowledge that limitation.

---

# 📊 Security Verdicts

ThreatLens supports four primary verdicts.

| Verdict | Meaning |
|---|---|
| 🟢 **SAFE** | Available evidence does not indicate significant malicious activity |
| 🟡 **SUSPICIOUS** | Evidence contains signals that warrant caution or further investigation |
| 🔴 **MALICIOUS** | Available evidence provides strong indications of malicious activity |
| ⚪ **UNKNOWN** | Available evidence is insufficient for a reliable assessment |

---

## 🟢 SAFE

A `SAFE` result means that the available intelligence did not identify strong malicious indicators.

It does **not** mean the target is guaranteed to be safe.

---

## 🟡 SUSPICIOUS

A `SUSPICIOUS` result indicates that one or more pieces of evidence warrant additional investigation.

---

## 🔴 MALICIOUS

A `MALICIOUS` result indicates that the available evidence provides strong indications of malicious activity.

---

## ⚪ UNKNOWN

An `UNKNOWN` result indicates that the available evidence is insufficient to make a reliable assessment.

This can occur when:

- Sources fail
- Evidence is incomplete
- Gemini is unavailable
- The response cannot be reliably interpreted

---

# 📈 Confidence Score

ThreatLens displays a confidence score between:

```text
0 - 100
```

Example:

```text
Confidence: 95%
```

The confidence score describes the confidence of the assessment based on the available evidence.

It should not be interpreted as a mathematical probability of maliciousness or safety.

---

# 📝 AI Security Assessment

After the verdict, ThreatLens displays an **AI Security Assessment**.

The assessment includes three major components.

---

## Summary

A concise explanation of what the available evidence indicates.

Example:

```text
The available intelligence does not show strong
indicators of malicious activity for this target.
```

---

## Key Findings

Important observations derived from the intelligence.

Example:

```text
• VirusTotal reported no significant malicious detections.
• Registration information was available.
• No strong malicious indicators were identified.
```

---

## Recommendation

A practical next step based on the available evidence.

Example:

```text
No immediate blocking action is indicated based on
the available evidence, but normal security monitoring
should continue.
```

---

# 📂 Source Evidence

ThreatLens displays the underlying intelligence separately from the AI assessment.

The interface contains expandable sections such as:

```text
Source Evidence

▶ VirusTotal

▶ WHOIS
```

Users can expand each source to manually inspect the information.

This provides transparency into the evidence behind the AI assessment.

---

# ✅ Input Validation

ThreatLens validates user input before sending requests to external services.

This reduces:

- Invalid API requests
- Unnecessary provider calls
- Malformed lookups
- Potentially unsafe input handling

---

# 🔐 URL Credential Protection

ThreatLens rejects URLs containing embedded credentials.

For example:

```text
https://username:password@example.com
```

is rejected.

This helps prevent accidental transmission or processing of credentials contained within user-supplied URLs.

---

# 🏗️ Application Architecture

ThreatLens uses a lightweight two-module Python architecture.

```text
┌──────────────────────────────┐
│            app.py            │
│                              │
│ • Streamlit UI               │
│ • Input handling             │
│ • Validation                 │
│ • Orchestration              │
│ • Gemini integration         │
│ • Result rendering           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          sources.py          │
│                              │
│ • VirusTotal                 │
│ • WHOIS/RDAP                 │
│ • Source registry            │
│ • Source normalization       │
└──────────────────────────────┘
```

The dependency direction is:

```text
app.py
   ↓
sources.py
```

The source layer does not depend on the Streamlit UI.

---

# 🧩 Registry-Based Source Architecture

ThreatLens uses a centralized source registry.

Conceptually:

```python
SOURCES = {
    "VirusTotal": get_virustotal,
    "WHOIS": get_whois,
}
```

The application can iterate over registered sources instead of hardcoding source calls throughout the application.

Conceptually:

```python
for source_name, source_function in SOURCES.items():
    result = source_function(target_type, target)
```

This makes the architecture easier to extend.

---

# ➕ Adding Future Intelligence Sources

A future source can be implemented as a function:

```python
def get_new_source(target_type, target):
    ...
```

and then registered:

```python
SOURCES["New Source"] = get_new_source
```

The architecture is intended to allow the new source to participate in the same general workflow:

```text
New Source
    ↓
Source Result
    ↓
Aggregated Evidence
    ↓
Gemini Prompt
    ↓
AI Assessment
    ↓
Source Evidence UI
```

This avoids rewriting the main application every time a new intelligence provider is added.

---

# 📦 Source Result Contract

Each source follows a common result structure.

Successful lookup:

```python
{
    "source": "VirusTotal",
    "success": True,
    "data": {
        # normalized source information
    },
    "error": None
}
```

Failed lookup:

```python
{
    "source": "VirusTotal",
    "success": False,
    "data": {},
    "error": "Human-readable error message"
}
```

This creates a consistent interface between intelligence providers and the application.

---

# 📁 Project Structure

The GitHub repository contains:

```text
threatlens/
│
├── app.py
├── sources.py
├── requirements.txt
└── README.md
```

---

# 📄 File Responsibilities

## `app.py`

The main Streamlit application.

It handles:

- Streamlit configuration
- User interface
- Target type selection
- Knowledge level selection
- Target input
- Input validation
- Target normalization
- Source orchestration
- Evidence aggregation
- Gemini prompt construction
- Gemini API communication
- Structured response parsing
- Verdict rendering
- Confidence rendering
- AI assessment rendering
- Source evidence rendering
- Session state
- Loading/status handling
- Error handling

---

## `sources.py`

The intelligence-source layer.

It handles:

- VirusTotal integration
- WHOIS/RDAP integration
- Source-specific helper functions
- Source result normalization
- Central source registry

It does not contain the main Streamlit UI.

---

## `requirements.txt`

Contains the Python packages required to run ThreatLens.

Typical dependencies include:

```text
streamlit
requests
google-genai
whois-python
ipwhois
```

The exact versions used by the project should remain defined by the repository's current `requirements.txt`.

---

## `README.md`

Project documentation containing:

- Project overview
- Features
- Architecture
- Installation
- Configuration
- Deployment
- Testing
- Security information
- Limitations
- Usage information

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application framework |
| VirusTotal API | Threat intelligence and reputation |
| WHOIS/RDAP | Domain and IP registration/network intelligence |
| Google Gemini | AI-assisted evidence interpretation |
| Requests | HTTP/API communication |
| `ipaddress` | IP address validation |
| `urllib.parse` | URL parsing |

---

# 📦 Requirements

ThreatLens requires Python and the packages listed in:

```text
requirements.txt
```

Typical packages include:

```text
streamlit
requests
google-genai
whois-python
ipwhois
```

---

# 🔑 API Keys

ThreatLens requires API credentials for the external services it uses.

The main credentials are:

```text
VIRUSTOTAL_API_KEY
GEMINI_API_KEY
```

---

# 🔐 API Key Security

Never place actual keys in:

```text
app.py
sources.py
README.md
```

Never commit a real key to GitHub.

Do not create code such as:

```python
VIRUSTOTAL_API_KEY = "real-secret-key"
```

Instead, use Streamlit secrets or environment variables.

---

# ☁️ Streamlit Community Cloud Deployment

ThreatLens can be deployed directly from GitHub using Streamlit Community Cloud.

The repository should contain:

```text
app.py
sources.py
requirements.txt
README.md
```

---

# 🚀 Streamlit Deployment Flow

The complete deployment flow is:

```text
GitHub Repository
       │
       ▼
app.py
       │
       ├── sources.py
       │
       └── requirements.txt
       │
       ▼
Streamlit Community Cloud
       │
       ▼
Configure Secrets
       │
       ├── VIRUSTOTAL_API_KEY
       └── GEMINI_API_KEY
       │
       ▼
Deploy
       │
       ▼
ThreatLens Web Application
```

---

# 🔒 Deployment Security

Before deploying publicly:

### Check that API keys are not present in:

```text
app.py
sources.py
README.md
Git history
```

# 🧪 Example Test Cases

## Test 1 — IPv4

```text
Target Type:
IP Address

Knowledge Level:
Beginner

Target:
8.8.8.8
```

Expected behavior:

- IP validation succeeds
- VirusTotal lookup is attempted
- WHOIS/RDAP lookup is attempted where supported
- Evidence is displayed
- Gemini assessment is generated if available

---

# Test 2 — Invalid IPv4

```text
Target Type:
IP Address

Target:
999.999.999.999
```

Expected behavior:

```text
Validation error
```

The invalid target should not be sent to external intelligence providers.

---

# Test 3 — Invalid URL Scheme

```text
Target Type:
URL

Target:
ftp://example.com
```

Expected behavior:

```text
URL must use http:// or https://
```

---

# 📊 Example Result

A successful result can look conceptually like:

```text
ANALYSIS RESULT

SAFE

Confidence: 95%

Assessment based on the available intelligence;
not an absolute security guarantee.
```

The application then provides:

```text
AI Security Assessment

Summary
The available intelligence does not show strong
indicators of malicious activity.

Key Findings
• VirusTotal evidence was reviewed.
• WHOIS/RDAP evidence was reviewed.
• No strong malicious indicators were identified.

Recommendation
No immediate blocking action is indicated based
on the available evidence. Continue normal security
monitoring.
```

Then:

```text
Source Evidence

▶ VirusTotal

▶ WHOIS
```

---

# 🛡️ Security Recommendations

When using ThreatLens in a real environment:

1. Keep API keys private.
2. Use Streamlit secrets for deployed applications.
3. Never commit secrets to GitHub.
4. Rotate credentials if they are accidentally exposed.
5. Review the underlying source evidence.
6. Do not rely exclusively on the AI verdict.
7. Treat `SAFE` as an intelligence assessment rather than a guarantee.
8. Treat `UNKNOWN` as insufficient evidence rather than maliciousness.
9. Use additional security controls for high-impact decisions.
10. Monitor API usage and provider rate limits.

---

# 📐 Architecture Summary

The core architecture can be summarized as:

```text
                     THREATLENS
                         │
                         ▼
                ┌────────────────┐
                │  Streamlit UI  │
                └───────┬────────┘
                        │
                        ▼
                ┌────────────────┐
                │ Input Validator│
                └───────┬────────┘
                        │
                        ▼
                ┌────────────────┐
                │ Source Registry│
                └───────┬────────┘
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
      ┌──────────────┐      ┌──────────────┐
      │  VirusTotal  │      │ WHOIS / RDAP │
      └──────┬───────┘      └──────┬───────┘
             │                     │
             └──────────┬──────────┘
                        ▼
                ┌────────────────┐
                │    Evidence    │
                │   Aggregation  │
                └───────┬────────┘
                        │
                        ▼
                ┌────────────────┐
                │ Google Gemini  │
                └───────┬────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ Security Assessment  │
             │                      │
             │ Verdict              │
             │ Confidence           │
             │ Summary              │
             │ Findings             │
             │ Recommendation       │
             └──────────┬───────────┘
                        │
                        ▼
                ┌────────────────┐
                │ Source Evidence│
                └────────────────┘
```

---

# 📊 Expected Application Experience

The user interface follows a simple workflow:

```text
ThreatLens

IP, Domain & URL Safety Intelligence

Analyze an IP address, domain, or URL using
VirusTotal and WHOIS evidence.

Target Type
[ IP Address ▼ ]

Knowledge Level
[ Beginner ▼ ]

Target
[ 8.8.8.8 ]

[ Analyze ]
```

After analysis:

```text
Analysis Result

SAFE

Confidence: 95%

Assessment based on the available intelligence;
not an absolute security guarantee.
```

Then:

```text
AI Security Assessment

Summary

...

Key Findings

• ...
• ...
• ...

Recommendation

...
```

Finally:

```text
Source Evidence

▶ VirusTotal

▶ WHOIS
```

---

# 👨‍💻 Author

**ThreatLens**

IP, Domain & URL Safety Intelligence

Built with:

```text
Python
+
Streamlit
+
VirusTotal
+
WHOIS/RDAP
+
Google Gemini
```

---

# ⭐ Project Summary

ThreatLens combines threat intelligence and AI-assisted analysis into a simple cybersecurity dashboard.

The application follows this model:

```text
             USER INPUT
                 │
                 ▼
        ┌─────────────────┐
        │ IP / Domain /   │
        │      URL        │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │    Validation   │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   VirusTotal    │
        │       +         │
        │   WHOIS/RDAP    │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Evidence        │
        │ Aggregation     │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Google Gemini   │
        │ AI Assessment   │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Verdict         │
        │ Confidence      │
        │ Findings        │
        │ Recommendation  │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Source Evidence │
        └─────────────────┘
```

**ThreatLens — turning IP, domain, and URL intelligence into understandable security insight.**
