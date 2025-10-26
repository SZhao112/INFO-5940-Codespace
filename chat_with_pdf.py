import streamlit as st
import os
from openai import OpenAI
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# setup API credentials
os.environ['OPENAI_API_KEY'] = os.environ.get("API_KEY", "")
os.environ['OPENAI_BASE_URL'] = 'https://api.ai.it.cornell.edu'

client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)

def extract_text_from_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()

    if ext == 'pdf':
        reader = PdfReader(uploaded_file)
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        return '\n'.join(parts)
    elif ext in ['txt', 'md']:
        return uploaded_file.read().decode("utf-8")

    return None

def chunk_documents(text_content, filename):
    # wrap text in Document object
    doc = Document(page_content=text_content, metadata={"source": filename})

    # split into chunks with overlap
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents([doc])
    return chunks

def create_vectorstore(docs):
    # create embeddings using openai model
    emb = OpenAIEmbeddings(model="openai.text-embedding-3-large")

    # build vector store from documents
    vs = Chroma.from_documents(documents=docs, embedding=emb)
    return vs

def retrieve_context(vs, query, k=5):
    # search for similar chunks
    results = vs.similarity_search(query, k=k)
    return results

st.set_page_config(page_title="Document Q&A", page_icon="📚", layout="wide")
st.title("📝 File Q&A with OpenAI")

# init session state
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = {}

# sidebar for file uploads
with st.sidebar:
    st.header("Document Upload")

    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["txt", "md", "pdf"],
        accept_multiple_files=True,
        help="Upload .txt, .md, or .pdf files"
    )

    if uploaded_files:
        # only process files we haven't seen before
        new_files = [f for f in uploaded_files if f.name not in st.session_state.uploaded_docs]

        if new_files:
            with st.spinner("Processing documents..."):
                all_docs = []

                for f in new_files:
                    text = extract_text_from_file(f)
                    if text:
                        chunks = chunk_documents(text, f.name)
                        all_docs.extend(chunks)

                        st.session_state.uploaded_docs[f.name] = {
                            "chunks": len(chunks),
                            "size": len(text)
                        }

                if all_docs:
                    # create new vectorstore or add to existing one
                    if st.session_state.vectorstore is None:
                        st.session_state.vectorstore = create_vectorstore(all_docs)
                    else:
                        st.session_state.vectorstore.add_documents(all_docs)

                    st.success(f"Processed {len(new_files)} document(s)")

    # show uploaded docs
    if st.session_state.uploaded_docs:
        st.subheader("Uploaded Documents")
        for fname, info in st.session_state.uploaded_docs.items():
            st.text(f"📄 {fname}")
            st.caption(f"  {info['chunks']} chunks")

    # clear button
    if st.button("Clear All"):
        st.session_state.uploaded_docs = {}
        st.session_state.vectorstore = None
        st.session_state.messages = []
        st.rerun()

# chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# show initial prompt only when empty
if not st.session_state.messages and st.session_state.vectorstore is None:
    st.info("💬 You can chat directly or 👈 upload documents for document-based Q&A")

# display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(msg["content"])

# chat input
q = st.chat_input("Ask a question")

if q:
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user", avatar="🧑"):
        st.write(q)

    with st.chat_message("assistant", avatar="🤖"):
        # if we have docs, use RAG
        if st.session_state.vectorstore is not None:
            with st.spinner("Retrieving relevant information..."):
                chunks = retrieve_context(st.session_state.vectorstore, q, k=5)

            # build context from retrieved chunks
            ctx = "\n\n".join([
                f"[Source: {doc.metadata['source']}]\n{doc.page_content}"
                for doc in chunks
            ])

            prompt = f"""You are a helpful assistant. Answer questions based on the provided document context.
Use only the information from the context below. If you cannot find the answer in the context, say so.

Context:
{ctx}"""

            msgs = [
                {"role": "system", "content": prompt}
            ] + st.session_state.messages
        else:
            # no docs, just chat normally
            msgs = st.session_state.messages

        stream = client.chat.completions.create(
            model="openai.gpt-4o",
            messages=msgs,
            stream=True
        )
        resp = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": resp})