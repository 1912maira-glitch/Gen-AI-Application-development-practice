# ✍️ AI Content Assistant

An AI-powered content generation application that helps users create **tailored social media posts, captions, and hashtags** based on their selected platform, content type, tone, target audience, and topic.

The application uses **Streamlit** for the user interface, **Groq API** for AI-powered generation, and the **openai/gpt-oss-120b** model to generate high-quality content.

---

## 🚀 Features

- ✍️ Generate AI-powered content instantly
- 📱 Support multiple content platforms
- 🎯 Select a specific content type
- 🎨 Customize the writing tone
- 👥 Define a target audience
- 📝 Provide a topic or key points
- #️⃣ Automatically generate relevant hashtags
- 📢 Include a hook, main body, and Call to Action (CTA)
- 🔐 Secure API key input using password-type field
- ⚡ Fast content generation using Groq
- 💻 Simple and clean Streamlit interface
- ❌ Built-in validation for missing API keys and topics
- ⚠️ Error handling for API or generation failures

---

## 🖥️ Supported Platforms

The application can generate content for:

- LinkedIn
- Instagram
- Twitter / X
- Facebook
- Blog Posts

---

## 📝 Content Types

Users can select from:

- Educational
- Promotional
- Storytelling
- Opinion / Thought Leadership
- Announcement

---

## 🎨 Available Tones

The application supports:

- Professional
- Casual & Friendly
- Persuasive
- Witty & Humorous
- Inspirational

---

## 🧠 How It Works

The application follows a simple AI content generation workflow:

```text
User Input
    ↓
Select Platform
    ↓
Select Content Type
    ↓
Select Tone
    ↓
Enter Target Audience
    ↓
Enter Topic / Key Points
    ↓
Groq API
    ↓
openai/gpt-oss-120b
    ↓
AI Content Generation
    ↓
Generated Post + CTA + Hashtags

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Web UI
- **Groq API** – LLM API
- **openai/gpt-oss-120b** – Content generation
