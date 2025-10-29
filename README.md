# Assignment 1: Document Q&A Application

## Overview
This is a Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions about their content through a conversational interface.

## Running the Application

### Setup
1. Make sure you're in the Codespace with all dependencies installed.
2. Set your API key in .devcontainer/devcontainer.json and rebuild the environment
3. Install all required package from requirements.txt by

'''bash
pip install -r requirements.txt
'''


### Start the app
```bash
streamlit run chat_with_pdf.py
```

Click "Open in Browser" when the popup appears or use ctrl(cmd for MacOS)+click on the link showed in terminal

## Features

### File Upload
- Supports `.txt`, `.md`, and `.pdf` files
- Upload multiple documents at once
- Each document is automatically processed and indexed

### Chat Interface
- Ask questions about uploaded documents
- Or just chat normally without uploading anything
- Multi-turn conversations supported
- Responses are grounded in document content when docs are uploaded


### Technical Stack
- **UI**: Streamlit
- **LLM**: OpenAI GPT-4o (via Cornell API)
- **Embeddings**: OpenAI text-embedding-3-large
- **Vector DB**: ChromaDB
- **Document Processing**: LangChain (RecursiveCharacterTextSplitter)
- **PDF Parsing**: PyPDF

## Implementation Notes

### Edited requirements.txt
- Added `numpy<2.0,>=1.26.0`, `langchain-chroma`, `chromadb>=0.5` to requirements.

### Why These Choices?
- **Chunk size 500**: Balances context and specificity
- **Overlap 50**: Prevents cutting related information
- **k=5 retrieval**: Good amount of context without overwhelming the LLM
- **Direct RAG**: Simpler than LangGraph for this use case

### Known Limitations
- PDF parsing works best on text-based PDFs (not scanned images)
- Large documents may take a moment to process
- Vector store is stored in session (cleared on restart)   
