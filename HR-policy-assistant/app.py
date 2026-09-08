```python
import os
import re
from typing import List, Dict, Tuple

import faiss
import fitz  # PyMuPDF
import numpy as np
import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer


# ============================================================
# Configuration
# ============================================================

APP_TITLE = "HR Policy Assistant"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "openai/gpt-oss-120b"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 5


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📘",
    layout="wide",
)


# ============================================================
# Styling
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #666;
            margin-bottom: 1.5rem;
        }

        .source-box {
            padding: 0.8rem;
            border-radius: 0.5rem;
            border: 1px solid #ddd;
            margin-top: 0.5rem;
        }

        .answer-box {
            padding: 1rem;
            border-radius: 0.6rem;
            border: 1px solid #ddd;
            background-color: rgba(128, 128, 128, 0.05);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Cached resources
# ============================================================

@st.cache_resource(show_spinner="Loading embedding model...")
def load_embedding_model():
    """
    Load the Sentence Transformer once per Streamlit process.
    """
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


@st.cache_resource
def get_groq_client():
    """
    Create and cache the Groq client.
    Supports both Streamlit Cloud secrets and local environment variables.
    """

    api_key = None

    # Streamlit Cloud
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

    # Local development fallback
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


# ============================================================
# PDF processing
# ============================================================

def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """

    text = text.replace("\x00", " ")

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_pdf_pages(pdf_bytes: bytes) -> List[Dict]:
    """
    Extract text from every PDF page.

    Returns:
        [
            {
                "page": 1,
                "text": "..."
            },
            ...
        ]
    """

    pages = []

    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page_number, page in enumerate(pdf_document, start=1):
        text = page.get_text("text")
        text = clean_text(text)

        if text:
            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    pdf_document.close()

    return pages


# ============================================================
# Chunking
# ============================================================

def split_text(text: str, chunk_size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Split text into overlapping word-based chunks.
    """

    words = text.split()

    if not words:
        return []

    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def create_chunks(pages: List[Dict]) -> List[Dict]:
    """
    Convert PDF pages into chunks while preserving page metadata.
    """

    chunks = []

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"]

        page_chunks = split_text(text)

        for chunk_number, chunk in enumerate(page_chunks, start=1):
            chunks.append(
                {
                    "text": chunk,
                    "page": page_number,
                    "chunk": chunk_number,
                }
            )

    return chunks


# ============================================================
# FAISS index
# ============================================================

def build_faiss_index(
    chunks: List[Dict],
    embedding_model: SentenceTransformer,
) -> Tuple[faiss.Index, np.ndarray]:
    """
    Create normalized embeddings and a FAISS inner-product index.

    Normalized embeddings + inner product ~= cosine similarity.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False,
        normalize_embeddings=True,
    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    return index, embeddings


def search_faiss(
    query: str,
    index: faiss.Index,
    chunks: List[Dict],
    embedding_model: SentenceTransformer,
    top_k: int = TOP_K,
) -> List[Dict]:
    """
    Retrieve the most relevant chunks for a query.
    """

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx < 0 or idx >= len(chunks):
            continue

        result = chunks[idx].copy()
        result["score"] = float(score)

        results.append(result)

    return results


# ============================================================
# Prompt construction
# ============================================================

def build_context(results: List[Dict]) -> str:
    """
    Convert retrieved chunks into a context block for the LLM.
    """

    context_parts = []

    for i, result in enumerate(results, start=1):

        context_parts.append(
            f"""
SOURCE {i}
Page: {result["page"]}
Relevance score: {result["score"]:.4f}

{result["text"]}
""".strip()
        )

    return "\n\n---\n\n".join(context_parts)


def build_prompt(question: str, context: str) -> str:
    """
    Construct a grounded HR policy prompt.
    """

    return f"""
You are an HR Policy Assistant.

Answer the employee's question using ONLY the HR policy
information provided in the context below.

Rules:
1. Do not invent HR policies.
2. Do not use outside knowledge.
3. If the answer is not present in the provided context,
   clearly say that the uploaded HR policy does not provide
   enough information to answer the question.
4. Give a concise but useful answer.
5. When possible, mention the relevant policy section or page.
6. If the policy contains conditions, exceptions, eligibility
   requirements, or approval requirements, include them.
7. Do not claim that something is allowed or prohibited unless
   the policy supports that conclusion.
8. Treat the document as the source of truth.

HR POLICY CONTEXT
=================
{context}

EMPLOYEE QUESTION
=================
{question}

ANSWER
=================
""".strip()


# ============================================================
# Groq generation
# ============================================================

def generate_answer(
    question: str,
    results: List[Dict],
    groq_client: Groq,
) -> str:
    """
    Send retrieved context to Groq GPT-OSS 120B.
    """

    context = build_context(results)
    prompt = build_prompt(question, context)

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful HR policy question-answering "
                    "assistant. Ground every answer in the supplied "
                    "policy context."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=800,
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


# ============================================================
# Session state
# ============================================================

def initialize_session_state():

    defaults = {
        "document_name": None,
        "pages": None,
        "chunks": None,
        "faiss_index": None,
        "messages": [],
        "document_ready": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()


# ============================================================
# Header
# ============================================================

st.markdown(
    '<div class="main-title">📘 HR Policy Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Upload an HR policy PDF and ask questions about its contents."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuration")

    st.write(f"**LLM:** `{GROQ_MODEL}`")
    st.write(f"**Embeddings:** `{EMBEDDING_MODEL_NAME}`")
    st.write(f"**Vector DB:** `FAISS`")
    st.write(f"**PDF parser:** `PyMuPDF`")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload HR policy PDF",
        type=["pdf"],
        help="Upload the HR policy document you want to query.",
    )

    process_button = st.button(
        "Process PDF",
        type="primary",
        use_container_width=True,
    )

    if st.button(
        "Clear document",
        use_container_width=True,
    ):
        st.session_state.document_name = None
        st.session_state.pages = None
        st.session_state.chunks = None
        st.session_state.faiss_index = None
        st.session_state.messages = []
        st.session_state.document_ready = False

        st.rerun()


# ============================================================
# Process uploaded PDF
# ============================================================

if process_button:

    if uploaded_file is None:

        st.warning("Please upload an HR policy PDF first.")

    else:

        with st.spinner("Processing HR policy PDF..."):

            try:

                pdf_bytes = uploaded_file.getvalue()

                pages = extract_pdf_pages(pdf_bytes)

                if not pages:
                    st.error(
                        "No readable text was found in the PDF. "
                        "The document may be image-only/scanned."
                    )
                    st.stop()

                chunks = create_chunks(pages)

                if not chunks:
                    st.error("Could not create text chunks from the PDF.")
                    st.stop()

                embedding_model = load_embedding_model()

                faiss_index, _ = build_faiss_index(
                    chunks,
                    embedding_model,
                )

                st.session_state.document_name = uploaded_file.name
                st.session_state.pages = pages
                st.session_state.chunks = chunks
                st.session_state.faiss_index = faiss_index
                st.session_state.messages = []
                st.session_state.document_ready = True

                st.success(
                    f"Document processed successfully: "
                    f"{len(pages)} pages, {len(chunks)} chunks."
                )

            except Exception as e:

                st.error(
                    f"An error occurred while processing the PDF: {e}"
                )


# ============================================================
# Document status
# ============================================================

if st.session_state.document_ready:

    st.info(
        f"📄 **{st.session_state.document_name}**  |  "
        f"{len(st.session_state.pages)} pages  |  "
        f"{len(st.session_state.chunks)} chunks indexed"
    )


# ============================================================
# API key check
# ============================================================

groq_client = get_groq_client()

if groq_client is None:

    st.warning(
        "Groq API key is not configured. "
        "Add `GROQ_API_KEY` to Streamlit Secrets before asking questions."
    )


# ============================================================
# Chat history
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("📚 Sources"):

                for source in message["sources"]:

                    st.markdown(
                        f"""
                        **Page {source["page"]}**
                        
                        Relevance: `{source["score"]:.4f}`
                        
                        > {source["text"]}
                        """
                    )


# ============================================================
# Question input
# ============================================================

question = st.chat_input(
    "Ask a question about the HR policy..."
)


if question:

    if not st.session_state.document_ready:

        st.warning(
            "Please upload and process an HR policy PDF before asking questions."
        )
        st.stop()

    if groq_client is None:

        st.error(
            "Groq API key is missing. Configure `GROQ_API_KEY` "
            "in Streamlit Secrets."
        )
        st.stop()

    # Display user question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Retrieve relevant chunks
    with st.chat_message("assistant"):

        with st.spinner("Searching the HR policy..."):

            embedding_model = load_embedding_model()

            results = search_faiss(
                query=question,
                index=st.session_state.faiss_index,
                chunks=st.session_state.chunks,
                embedding_model=embedding_model,
                top_k=TOP_K,
            )

        if not results:

            answer = (
                "I could not find relevant information in the "
                "uploaded HR policy."
            )

            sources = []

        else:

            with st.spinner("Generating answer..."):

                try:

                    answer = generate_answer(
                        question=question,
                        results=results,
                        groq_client=groq_client,
                    )

                    sources = results

                except Exception as e:

                    answer = (
                        "I encountered an error while generating "
                        f"the answer: {e}"
                    )

                    sources = []

        st.markdown(answer)

        if sources:

            with st.expander("📚 Sources"):

                for source in sources:

                    st.markdown(
                        f"""
                        **Page {source["page"]}**
                        
                        Relevance: `{source["score"]:.4f}`
                        
                        > {source["text"]}
                        """
                    )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )
```

This uses the official Groq Python client and the `openai/gpt-oss-120b` model ID documented by Groq.
