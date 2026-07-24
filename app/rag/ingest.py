from app.services.rag_store import build_vectorstore

if __name__ == "__main__":
    print(f"Indexed {build_vectorstore()} chunks")