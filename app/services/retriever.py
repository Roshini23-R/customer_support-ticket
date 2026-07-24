from app.services.rag_store import get_vectorstore

def retrieve_context(query: str, k: int = 3) -> str:
    try:
        db = get_vectorstore()
        docs = db.similarity_search(query, k=k)
    except Exception:
        return ""
    return "\n\n".join([d.page_content for d in docs]) if docs else ""