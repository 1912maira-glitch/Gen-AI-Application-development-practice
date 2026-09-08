# 📚 HR Policy Assistant

An AI-powered **RAG (Retrieval-Augmented Generation) application** that allows users to upload an HR policy PDF and ask questions about its contents.

The application retrieves relevant information from the uploaded document using **Sentence Transformers and FAISS**, then generates grounded answers using the **Groq `openai/gpt-oss-120b` model**.

## ✨ Features

- 📄 Upload HR policy PDF documents
- 🔍 Extract PDF text using PyMuPDF
- ✂️ Split documents into overlapping text chunks
- 🧠 Generate semantic embeddings using Sentence Transformers
- ⚡ Perform similarity search using FAISS
- 🤖 Generate grounded answers using Groq `openai/gpt-oss-120b`
- 💬 Interactive Streamlit chat interface
- 📚 Display retrieved sources and page numbers
- ⚙️ Adjustable chunk size, overlap, and number of retrieved chunks
- ☁️ Deployable on Streamlit Community Cloud

## 🏗️ RAG Architecture

    HR Policy PDF
          ↓
       PyMuPDF
          ↓
     Text Extraction
          ↓
        Chunking
          ↓
    Sentence Transformers
          ↓
       Embeddings
          ↓
         FAISS
          ↓
    Relevant Chunks
          ↓
    Groq GPT-OSS 120B
          ↓
     Grounded Answer

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | User interface |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Groq API | LLM inference |
| GPT-OSS 120B | Answer generation |
| GitHub | Version control |
| Streamlit Community Cloud | Deployment |

## 📁 Project Structure

    hr-policy-rag-assistant/
    │
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    │
    └── .streamlit/
        └── secrets.toml

> ⚠️ `secrets.toml` contains the Groq API key and must never be committed to GitHub.

## ⚙️ Installation

### 1. Clone the Repository

    git clone https://github.com/your-username/hr-policy-rag-assistant.git
    cd hr-policy-rag-assistant

### 2. Install Dependencies

    pip install -r requirements.txt

### 3. Configure Groq API Key

Create the following file:

    .streamlit/secrets.toml

Add your API key:

    GROQ_API_KEY = "your_groq_api_key"

### 4. Run the Application

    streamlit run app.py

The application will open in your browser.

## 🔄 How It Works

### 1. PDF Upload

The user uploads an HR policy PDF through the Streamlit interface.

### 2. Text Extraction

PyMuPDF extracts readable text from the PDF pages.

### 3. Text Chunking

The extracted text is divided into smaller overlapping chunks to make retrieval more effective.

### 4. Embedding Generation

Sentence Transformers converts each text chunk into a numerical vector representation.

### 5. FAISS Indexing

The embeddings are stored in a FAISS index for fast semantic similarity search.

### 6. Retrieval

When the user asks a question, the question is converted into an embedding and FAISS retrieves the most relevant document chunks.

### 7. Answer Generation

The retrieved chunks are provided as context to the Groq `openai/gpt-oss-120b` model, which generates a grounded answer.

## 🧪 Example Questions

    What is the attendance policy?
    What is the leave policy?
    What is the probation period?
    What is the notice period?
    What are the working hours?
    What are the employee responsibilities?

The assistant should answer using information available in the uploaded HR policy document.


## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud**.

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select the `main` branch.
5. Select `app.py` as the main file.
6. Add `GROQ_API_KEY` under Streamlit Secrets.
7. Deploy the application.

After deployment, Streamlit provides a public URL for the application.

## ⚠️ Limitations

- Works best with text-based PDFs.
- Scanned or image-based PDFs require OCR.
- Answers depend on the quality of retrieved document chunks.
- The FAISS index is stored temporarily in memory.
- Uploaded documents are not permanently stored.
- Each new document creates a new temporary vector index.

## 🎯 Learning Goals

This project demonstrates practical skills in:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Semantic search
- Text embeddings
- Vector databases
- FAISS similarity search
- PDF processing
- Prompt engineering
- Streamlit development
- Groq API integration
- Git and GitHub
- Cloud deployment
- API key and secrets management

🚀 Live Application Demo: https://gen-ai-application-development-hr-policy-assistant.streamlit.app/
