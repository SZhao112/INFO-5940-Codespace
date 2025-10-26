# Reference Log

## External Resources Used

### Documentation
- **Streamlit docs** (https://docs.streamlit.io/)
  - Looked up `st.file_uploader` for multiple file support
  - Checked `st.chat_message` and `st.chat_input` for chat UI
  - Used `st.session_state` examples for state management

- **LangChain docs** (https://python.langchain.com/)
  - RecursiveCharacterTextSplitter configuration
  - Document class and metadata structure
  - Chroma vectorstore setup

- **PyPDF docs** (https://pypdf.readthedocs.io/)
  - PdfReader usage for extracting text from PDFs
  - Iterating through pages

- **OpenAI API docs** (https://platform.openai.com/docs/)
  - Streaming chat completions
  - Model names for Cornell API

### Code Examples
- Started from `langgraph_chroma_retreiver.ipynb` provided in class repo
  - Used it to figure out correct model names (`openai.gpt-4o` and `openai.text-embedding-3-large`)
  - Copied the vectorstore setup pattern
  - Adapted the chunking approach

- Original `chat_with_pdf.py` template
  - Had basic file upload and OpenAI chat
  - Extended it to support multiple files and PDF

## Problems Encountered

### Issue 1: PDF text extraction
First tried to just use `page.extract_text()` but some PDFs returned None for certain pages. Added a check to filter out empty pages before joining.

### Issue 2: Model names
Initially used `gpt-4o` and `text-embedding-3-large` without the `openai.` prefix. Got 400 errors. Checked the notebook and saw they use the prefix for Cornell's API.

### Issue 3: Vectorstore updates
When uploading multiple files, first version kept recreating the vectorstore and losing previous docs. Fixed by checking if vectorstore exists and using `add_documents()` instead.

### Issue 4: Chunking approach
Started using `split_text()` but it lost the Document metadata. Switched to `split_documents()` like in the notebook to preserve source info.

### Issue 5: numpy version conflict
Got weird errors about numpy dtypes when running streamlit. Googled the error and found it's a compatibility issue. Added `numpy<2.0` to requirements.

### Issue 6: Import errors
First used `from langchain_community.vectorstores import Chroma` but got import errors. Checked notebook again and saw it uses `from langchain_chroma import Chroma`. Changed imports to match.

## AI Tool Usage

Used **ChatGPT** for:
- Question: "How to upload multiple files in streamlit and track which ones are new?"
  - Got suggestion to use list comprehension with session state
  - Used: `new_files = [f for f in uploaded_files if f.name not in uploaded_docs]`

- Question: "Why is my streamlit app showing info message after every chat?"
  - Realized I needed to check if messages list is empty before showing prompt
  - Added: `if not st.session_state.messages and st.session_state.vectorstore is None`

Used **Claude** (Anthropic) for:
- Questions like "How to make the notification disappear in streamlit chat?"
  - Learned about avatar parameter in `st.chat_message()`

- Debugging numpy error traceback
  - Pasted the error, asked what version to use
  - Got recommendation for `numpy<2.0,>=1.26.0`

- Write the document base on my given information

## Implementation Decisions

### Chunk size
Tried different sizes (200, 500, 800). Went with 500 because:
- 200 was too small, lost context
- 800 sometimes cut sentences weirdly
- 500 seemed like good balance

Set overlap to 50 (10%) to avoid cutting related content.

### Retrieval k value
Using k=5 for retrieval. Tested with 3, 5, and 10.
- 3 sometimes missed relevant info
- 10 was too much context, slower responses
- 5 works well


### Session state structure
Store:
- `vectorstore`: the Chroma vector DB
- `uploaded_docs`: dict mapping filename to {chunks, size} for UI display
- `messages`: list of chat messages

Keeps track of everything between reruns.

### UI choices
- Sidebar for uploads keeps main area clean
- Show chunk count so user knows processing happened
- Clear button to reset every uploaded file
- Initial info message only shows when empty (not after every message)


## Key Learnings
1. Always check working examples (notebook) for exact API usage
2. Cornell's OpenAI endpoint needs `openai.` prefix on models
3. Session state is crucial for Streamlit apps that rerun constantly
4. Dependency versions matter a lot (numpy issue)
5. RAG doesn't have to be complicated - retrieve, context, generate
