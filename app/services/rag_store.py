from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import DOCS_DIR, CHROMA_DIR

def load_documents():
    docs = []
    if DOCS_DIR.exists():
        docs.extend(DirectoryLoader(str(DOCS_DIR), glob="**/*.txt", loader_cls=TextLoader).load())
        docs.extend(DirectoryLoader(str(DOCS_DIR), glob="**/*.pdf", loader_cls=PyPDFLoader).load())
    return docs

def build_vectorstore():
    docs = load_documents()
    if not docs:
        return 0

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    if not chunks:
        return 0

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Chroma.from_documents(chunks, embeddings, persist_directory=str(CHROMA_DIR))
    return len(chunks)

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return Chroma(persist_directory=str(CHROMA_DIR), embedding_function=embeddings)