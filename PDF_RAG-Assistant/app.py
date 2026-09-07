import os
from io import BytesIO

import faiss
import numpy as np
import streamlit as st
from groq import Groq
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# -----------------------------
# Configuration
# -----------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.3-70b-versatile"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
TOP_K = 5


# -----------------------------
# Cached models / clients
# -----------------------------
@st.cache_resource
def load_embedding_model():
    """Load the open embedding model once per Streamlit process."""
    return SentenceTransformer(EMBEDDING_MODEL)


def get_groq_api_key():
    """Read the Groq API key from Streamlit secrets or an environment variable."""
    try:
        key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        key = None

    return key or os.getenv("GROQ_API_KEY")


@st.cache_resource
def get_groq_client(api_key):
    return Groq(api_key=api_key)


# -----------------------------
# PDF extraction
# -----------------------------
def extract_pdf_pages(uploaded_file):
    """Extract text page-by-page so retrieved chunks can show page numbers."""
    pdf_bytes = uploaded_file.getvalue()
    reader = PdfReader(BytesIO(pdf_bytes))

    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())

        if text:
            pages.append(
                {
                    "page": page_number,
                    "text": text,
                }
            )

    return pages


# -----------------------------
# Token-based chunking
# -----------------------------
def chunk_text(text, tokenizer, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """
    Split text using the embedding model's tokenizer.

    This makes chunk size token-based rather than character-based.
    """
    token_ids = tokenizer.encode(text, add_special_tokens=False)

    if not token_ids:
        return []

    step = max(1, chunk_size - overlap)
    chunks = []

    for start in range(0, len(token_ids), step):
        chunk_ids = token_ids[start : start + chunk_size]
        if not chunk_ids:
            break

        chunk = tokenizer.decode(
            chunk_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        ).strip()

        if chunk:
            chunks.append(chunk)

        if start + chunk_size >= len(token_ids):
            break

    return chunks


def build_chunks(pages, tokenizer):
    """Create token-based chunks while preserving PDF page metadata."""
    chunks = []

    for page_data in pages:
        page_chunks = chunk_text(page_data["text"], tokenizer)

        for chunk_number, chunk in enumerate(page_chunks, start=1):
            chunks.append(
                {
                    "text": chunk,
                    "page": page_data["page"],
                    "chunk": chunk_number,
                }
            )

    return chunks


# -----------------------------
# Embeddings + FAISS
# -----------------------------
def build_faiss_index(chunks, embedding_model):
    """Embed all chunks and create a cosine-similarity FAISS index."""
    texts = [item["text"] for item in chunks]

    embeddings = embedding_model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(embeddings, dtype="float32")

    # With normalized vectors, inner product == cosine similarity.
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index


def retrieve(query, index, chunks, embedding_model, top_k=TOP_K):
    """Retrieve the most semantically similar chunks."""
    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    query_embedding = np.asarray(query_embedding, dtype="float32")

    k = min(top_k, len(chunks))
    scores, indices = index.search(query_embedding, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        item = dict(chunks[idx])
        item["score"] = float(score)
        results.append(item)

    return results


# -----------------------------
# Groq answer generation
# -----------------------------
def generate_answer(question, retrieved_chunks, groq_client):
    """Ask Groq to answer only from the retrieved PDF context."""
    context_parts = []

    for i, item in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Source {i} | PDF page {item['page']} | "
            f"retrieval score {item['score']:.3f}]\n{item['text']}"
        )

    context = "\n\n".join(context_parts)

    system_prompt = """You are a document question-answering assistant.

Answer the user's question using ONLY the supplied PDF context.

Rules:
1. Do not invent facts that are not supported by the context.
2. If the context does not contain enough information, say:
   "I couldn't find enough information in the uploaded PDF to answer that."
3. Be concise but useful.
4. When possible, cite the relevant PDF page number(s).
5. Distinguish clearly between information stated in the PDF and any uncertainty.
"""

    user_prompt = f"""PDF context:

{context}

Question:
{question}
"""

    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    return completion.choices[0].message.content


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📄",
    layout="wide",
)

st.title("📄 PDF RAG Assistant")
st.caption(
    "Upload a PDF → extract text → tokenize and chunk → embed → search with FAISS → answer with Groq."
)

with st.sidebar:
    st.header("⚙️ RAG Configuration")

    st.markdown("### 🔎 Retrieval")
    top_k = st.slider(
        "Retrieved chunks",
        min_value=2,
        max_value=10,
        value=TOP_K,
        help="Number of relevant PDF chunks retrieved before sending context to the LLM.",
    )

    st.caption(
        "Higher values provide more context, while lower values keep the prompt smaller."
    )

    st.divider()

    st.markdown("### 🤖 Language Model")
    st.write(f"`{GROQ_MODEL}`")
    st.caption("Open-weight model hosted by Groq")

    st.divider()

    st.markdown("### 🧠 Embedding Model")
    st.write(f"`{EMBEDDING_MODEL}`")
    st.caption("Runs locally in the Streamlit app")

    st.divider()

    st.markdown("### 🛠️ Technology Stack")
    st.write("• Streamlit")
    st.write("• PyPDF")
    st.write("• Sentence Transformers")
    st.write("• FAISS CPU")
    st.write("• Groq API")

    st.divider()

    st.markdown("### 📦 RAG Pipeline")
    st.caption("PDF → Extract → Chunk → Embed → FAISS → Retrieve → LLM")

    st.divider()

    st.markdown("### ⚙️ Configuration")
    st.write(f"Chunk size: `{CHUNK_SIZE}` tokens")
    st.write(f"Chunk overlap: `{CHUNK_OVERLAP}` tokens")

api_key = get_groq_api_key()

if not api_key:
    st.warning(
        "Groq API key not found. Add `GROQ_API_KEY` to Streamlit Secrets "
        "before asking questions."
    )

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    help="The PDF is processed in memory for this Streamlit session.",
)

if uploaded_file is not None:
    if not api_key:
        st.stop()

    file_signature = (
        uploaded_file.name,
        uploaded_file.size,
    )

    if st.session_state.get("file_signature") != file_signature:
        with st.spinner("Processing PDF..."):
            try:
                embedding_model = load_embedding_model()

                pages = extract_pdf_pages(uploaded_file)

                if not pages:
                    st.error(
                        "No extractable text was found. This may be a scanned/image-only PDF. "
                        "OCR would be required for that type of document."
                    )
                    st.stop()

                tokenizer = embedding_model.tokenizer
                chunks = build_chunks(pages, tokenizer)

                if not chunks:
                    st.error("The PDF did not produce any usable text chunks.")
                    st.stop()

                index = build_faiss_index(chunks, embedding_model)

                st.session_state.file_signature = file_signature
                st.session_state.pages = pages
                st.session_state.chunks = chunks
                st.session_state.index = index
                st.session_state.messages = []

            except Exception as exc:
                st.exception(exc)
                st.stop()

    pages = st.session_state["pages"]
    chunks = st.session_state["chunks"]
    index = st.session_state["index"]

    col1, col2, col3 = st.columns(3)
    col1.metric("PDF pages", len(pages))
    col2.metric("Text chunks", len(chunks))
    col3.metric("Chunk size", f"{CHUNK_SIZE} tokens")

    st.success(f"Indexed `{uploaded_file.name}` successfully.")

    st.divider()
    st.subheader("Ask questions about your PDF")

    # Display previous messages.
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask something about the uploaded PDF...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the PDF and generating an answer..."):
                try:
                    embedding_model = load_embedding_model()
                    groq_client = get_groq_client(api_key)

                    retrieved = retrieve(
                        question,
                        index,
                        chunks,
                        embedding_model,
                        top_k=top_k,
                    )

                    answer = generate_answer(
                        question,
                        retrieved,
                        groq_client,
                    )

                    st.markdown(answer)

                    with st.expander("Retrieved context"):
                        for i, item in enumerate(retrieved, start=1):
                            st.markdown(
                                f"**Source {i} — page {item['page']} "
                                f"(score: {item['score']:.3f})**"
                            )
                            st.write(item["text"])

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )

                except Exception as exc:
                    st.error(f"Something went wrong: {exc}")

else:
    st.info("Upload a PDF above to build your RAG index.")
