# 🛡️ ThreatLens

## IP, Domain & URL Safety Intelligence

ThreatLens is a lightweight cybersecurity intelligence application built with **Python and Streamlit**.

It allows users to analyze an **IP address, domain, or URL** using **VirusTotal** and **WHOIS/RDAP** intelligence. The collected evidence is then interpreted by **Google Gemini** to produce an evidence-based security assessment with a clear verdict, confidence score, key findings, and recommended next steps.

ThreatLens is intentionally designed to be **modular, lightweight, secure, and easy to extend**.

---

## 🚀 Overview

ThreatLens provides a single interface for investigating potentially suspicious infrastructure.

A user can:

- Select an IP address, domain, or URL
- Select a cybersecurity knowledge level
- Submit the target for analysis
- Validate the target before external lookups
- Collect VirusTotal intelligence
- Collect WHOIS/RDAP information
- Aggregate source evidence
- Generate an AI-assisted security assessment
- View a color-coded security verdict
- Review confidence and findings
- Inspect the underlying source evidence

The application is designed as an **intelligence lookup and analysis tool**, not as a web crawler or automated offensive security tool.

---

# ✨ Features

## Target Analysis

ThreatLens supports three target types:

### IP Address

Supports:

- IPv4
- IPv6

Example:

```text
8.8.8.8

## 📊 Security Verdicts

ThreatLens supports four verdicts:

Verdict	Meaning
🟢 SAFE	Available evidence does not indicate significant malicious activity
🟡 SUSPICIOUS	Evidence contains signals that warrant caution or further investigation
🔴 MALICIOUS	Available evidence provides strong indications of malicious activity
⚪ UNKNOWN	Evidence is insufficient for a reliable assessment
