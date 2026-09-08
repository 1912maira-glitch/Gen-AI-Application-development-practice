import streamlit as st
import fitz  # PyMuPDF
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            color: #6b7280;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }

        .answer-box {
            padding: 1.2rem;
            border-radius: 10px;
            border: 1px solid #ddd;
            background-color: #f8fafc;
        }

        .source-box {
            padding: 0.8rem;
            border-radius: 8px;
            background-color: #f1f5f9;
            margin-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📚 HR Policy Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask questions about your HR policy document using Retrieval-Augmented Generation (RAG).'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODELS
# ============================================================

@st.cache_resource
def load_embedding_model():
    """
    Load the Sentence Transformer embedding model.
    Cached so it isn't loaded on every Streamlit rerun.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def create_groq_client():
    """
    Create Groq API client using Streamlit secrets.
    """
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


embedding_model = load_embedding_model()
groq_client = create_groq_client()


# ============================================================
# SESSION STATE
# ============================================================

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "index" not in st.session_state:
    st.session_state.index = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_file):
    """
    Extract text from all pages of the uploaded PDF.

    Returns:
        list of dictionaries containing page number and text.
    """

    pdf_bytes = pdf_file.read()

    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text")

        if text.strip():
            pages.append(
                {
                    "page": page_number,
                    "text": text.strip()
                }
            )

    document.close()

    return pages


# ============================================================
# TEXT CHUNKING
# ============================================================

def create_chunks(pages, chunk_size=800, overlap=150):
    """
    Split PDF text into overlapping chunks.

    Each chunk keeps its original page number.
    """

    chunks = []

    for page in pages:

        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "page": page_number
                    }
                )

            start += chunk_size - overlap

    return chunks


# ============================================================
# CREATE FAISS INDEX
# ============================================================

def create_faiss_index(chunks):
    """
    Convert text chunks into embeddings and create
    a FAISS similarity search index.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=False
    )

    embeddings = embeddings.astype("float32")

    # Normalize embeddings so inner product behaves
    # like cosine similarity.
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


# ============================================================
# RETRIEVE RELEVANT CHUNKS
# ============================================================

def retrieve_relevant_chunks(query, index, chunks, top_k=4):
    """
    Search FAISS for the most relevant chunks.
    """

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype("float32")

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(chunks))
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        results.append(
            {
                "text": chunks[idx]["text"],
                "page": chunks[idx]["page"],
                "score": float(score)
            }
        )

    return results


# ============================================================
# GENERATE ANSWER WITH GROQ
# ============================================================

def generate_answer(question, retrieved_chunks):
    """
    Generate an answer using only the retrieved HR policy context.
    """

    if not retrieved_chunks:
        return (
            "I could not find relevant information in the uploaded "
            "HR policy document."
        )

    context_parts = []

    for result in retrieved_chunks:

        context_parts.append(
            f"[Page {result['page']}]\n{result['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an HR Policy Assistant.

Your task is to answer the user's question using ONLY the
provided HR policy context.

Rules:

1. Do not invent or assume information.
2. If the answer is not available in the context, clearly say:
   "The uploaded HR policy does not provide this information."
3. Give a concise but useful answer.
4. Mention relevant policy details when available.
5. Include page references when possible.
6. Do not use outside knowledge.
7. If the policy is ambiguous, explain the ambiguity instead
   of making a decision yourself.

HR POLICY CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a reliable HR policy assistant. "
                    "Always ground your answers in the provided "
                    "document context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=800
    )

    return response.choices[0].message.content


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📄 HR Policy Document")

    uploaded_file = st.file_uploader(
        "Upload HR Policy PDF",
        type=["pdf"]
    )

    st.divider()

    st.markdown("### ⚙️ RAG Settings")

    top_k = st.slider(
        "Number of retrieved chunks",
        min_value=2,
        max_value=8,
        value=4
    )

    chunk_size = st.slider(
        "Chunk size",
        min_value=400,
        max_value=1500,
        value=800,
        step=100
    )

    chunk_overlap = st.slider(
        "Chunk overlap",
        min_value=50,
        max_value=300,
        value=150,
        step=50
    )

    st.divider()

    if st.session_state.document_name:

        st.success(
            f"Loaded:\n{st.session_state.document_name}"
        )

        st.info(
            f"📑 Chunks: {len(st.session_state.chunks)}"
        )


# ============================================================
# PROCESS UPLOADED PDF
# ============================================================

if uploaded_file is not None:

    if (
        st.session_state.document_name
        != uploaded_file.name
    ):

        with st.spinner("Processing HR policy document..."):

            pages = extract_text_from_pdf(uploaded_file)

            if not pages:

                st.error(
                    "No readable text was found in this PDF. "
                    "The document may be scanned/image-based."
                )

                st.stop()

            chunks = create_chunks(
                pages,
                chunk_size=chunk_size,
                overlap=chunk_overlap
            )

            index = create_faiss_index(chunks)

            st.session_state.chunks = chunks
            st.session_state.index = index
            st.session_state.document_name = uploaded_file.name
            st.session_state.chat_history = []

        st.success(
            f"✅ Successfully processed "
            f"'{uploaded_file.name}'"
        )

        st.info(
            f"Extracted {len(pages)} pages and "
            f"created {len(chunks)} text chunks."
        )


# ============================================================
# API KEY CHECK
# ============================================================

if groq_client is None:

    st.warning(
        "⚠️ Groq API key is not configured. "
        "Add GROQ_API_KEY to Streamlit Secrets."
    )

    st.stop()


# ============================================================
# MAIN CHAT AREA
# ============================================================

if st.session_state.index is None:

    st.info(
        "👈 Upload an HR policy PDF from the sidebar "
        "to start asking questions."
    )

    st.markdown(
        """
        ### Example questions

        - What is the annual leave policy?
        - How many sick leaves are employees allowed?
        - What is the maternity leave policy?
        - What is the probation period?
        - What is the notice period?
        - Can employees work remotely?
        - What are the working hours?
        """
    )

else:

    st.subheader("💬 Ask about the HR policy")

    # Display previous messages
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about the HR policy..."
    )

    if question:

        # Display user question
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        # Retrieve relevant chunks
        with st.spinner("Searching HR policy..."):

            retrieved_chunks = retrieve_relevant_chunks(
                question,
                st.session_state.index,
                st.session_state.chunks,
                top_k=top_k
            )

        # Generate answer
        with st.chat_message("assistant"):

            with st.spinner("Generating answer..."):

                answer = generate_answer(
                    question,
                    retrieved_chunks
                )

            st.markdown(
                f'<div class="answer-box">{answer}</div>',
                unsafe_allow_html=True
            )

            # Show sources
            with st.expander("📚 View retrieved sources"):

                for i, result in enumerate(
                    retrieved_chunks,
                    start=1
                ):

                    st.markdown(
                        f"""
                        **Source {i} — Page {result['page']}**

                        Similarity score:
                        `{result['score']:.3f}`

                        <div class="source-box">
                        {result['text']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
