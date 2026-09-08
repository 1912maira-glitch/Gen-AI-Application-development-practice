# 📄 PDF RAG Assistant

A professional **Retrieval-Augmented Generation (RAG)** application that allows users to upload a PDF and ask questions about its content. The application retrieves relevant information from the document using semantic search and generates grounded answers using an open-weight LLM hosted by Groq.

## 🚀 Features

* 📤 Upload and process PDF documents
* ✂️ Token-based text chunking with overlap
* 🧠 Semantic embeddings using Sentence Transformers
* 🔎 Fast similarity search with FAISS
* 🤖 AI-powered answers using `openai/gpt-oss-120b` via Groq
* 📑 PDF page references in retrieved context
* 💬 Interactive Streamlit chat interface
* 🔐 Secure API key management with Streamlit Secrets

## 🏗️ RAG Pipeline

```text
PDF
 ↓
Text Extraction
 ↓
Token-based Chunking
 ↓
Sentence Transformer Embeddings
 ↓
FAISS Vector Index
 ↓
Semantic Retrieval
 ↓
Groq LLM
 ↓
Grounded Answer
```

## 🛠️ Tech Stack

| Technology            | Purpose                  |
| --------------------- | ------------------------ |
| Python                | Application development  |
| Streamlit             | Web interface            |
| PyPDF                 | PDF text extraction      |
| Sentence Transformers | Text embeddings          |
| FAISS                 | Vector similarity search |
| Groq API              | LLM inference            |
| GPT-OSS 120B          | Language model           |

## 📁 Project Structure

```text
pdf-rag-assistant/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Groq API Key

Set your API key as an environment variable:

```bash
GROQ_API_KEY="your_api_key"
```

Or use Streamlit Secrets:

```toml
GROQ_API_KEY = "your_api_key"
```

### 4. Run the application

```bash
streamlit run app.py
```

## ☁️ Deployment

The application can be deployed directly to **Streamlit Community Cloud**.

1. Push the project to GitHub.
2. Create a new Streamlit Cloud app.
3. Select your repository and `app.py`.
4. Add `GROQ_API_KEY` under **Secrets**.
5. Deploy.

```

## ⚠️ Limitations

* Currently designed for text-based PDFs.
* Scanned/image-only PDFs require OCR.
* FAISS indexes are created in memory during the session.
* Large documents may require additional optimization.

## 📌 Example Questions

After uploading a PDF, users can ask:

* What is the main topic of this document?
* Summarize the key findings.
* What does the document say about X?
* Which page discusses Y?
* Explain this concept in simple terms.

---

**Built with Python, Streamlit, FAISS, Sentence Transformers, and Groq.**

🚀 Live Application
Live Demo: https://gen-ai-application-development-pdf-rag-assistant.streamlit.app/

