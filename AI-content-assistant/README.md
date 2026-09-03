# ✍️ AI Content Assistant

An end-to-end, lightweight generative AI web application built with **Streamlit** and powered by **Groq's Ultra-Fast Inference Engine** running the **`gpt-oss-120b`** open-weights model. 

The application enables marketers, developers, and creators to instantly generate context-aware, platform-optimized social media posts, captions, call-to-actions, and relevant hashtags based on tailored user parameters.

---

## 📸 Overview & Interface
+-----------------------------------------------------------------------+
|  ✍️ AI Content Assistant                                              |
|  Generate tailored posts, captions, and hashtags instantly.          |
+-----------------------------------------------------------------------+
|  [Platform]      [Tone]          |  [Generated Output]                |
|  - LinkedIn      - Professional  |  🚀 I reclaimed my weekends by     |
|  - Instagram     - Casual        |  automating the boring stuff!      |
|  - Twitter / X   - Witty         |                                    |
|                                  |  - Hook & Storyline                |
|  [Content Type]  [Target]        |  - Structured Key Points           |
|  - Educational   - Developers    |  - Call To Action (CTA)            |
|  - Storytelling  - Marketers     |  - High-Reach Hashtags             |
+-----------------------------------------------------------------------+

---

## ✨ Key Features

* **Platform-Specific Optimization:** Native formatting and structure tailored for LinkedIn, Instagram, Twitter/X, Facebook, and Blog posts.
* **Custom Audience & Tone Alignment:** Tailors communication style (Professional, Casual, Persuasive, Witty, Inspirational) to match targeted demographic profiles.
* **Open-Source LLM Integration:** Leverages the open-weights **`openai/gpt-oss-120b`** model hosted on Groq for sub-second text generation latency.
* **Structured Output Pipeline:** Guarantees a compelling hook, organized body text, driving CTA, and relevant high-traffic hashtags.
* **Zero-Persistence Privacy:** Processes requests on-the-fly without storing sensitive user keys or content parameters in external databases.

---

## 🛠️ Tech Stack & Dependencies

* **Frontend Framework:** [Streamlit](https://streamlit.io/) (v1.30.0+)
* **Inference Engine:** [Groq Cloud API](https://console.groq.com/)
* **Foundation Model:** `openai/gpt-oss-120b`
* **Language:** Python 3.9+

---

## 🏗️ Architecture & Workflow

1. **User Input:** User specifies target platform, tone, audience, content category, and key topic parameters.
2. **Prompt Construction:** The application dynamic prompt generator compiles system guidelines and context rules.
3. **Groq Inference Engine:** Sends raw parameters via the Groq SDK to execute low-latency inference on the `openai/gpt-oss-120b` model.
4. **Rendering:** Markdown output with rich text formatting, emojis, and hashtags is displayed directly on the Streamlit interface.

---

## 🚀 Quickstart Guide

### Prerequisites
1. Python 3.9 or higher installed on your local machine.
2. A free Groq API key (Obtain one from [Groq Console](https://console.groq.com/)).

---
