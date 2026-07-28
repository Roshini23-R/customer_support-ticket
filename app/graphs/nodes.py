from app.services.classifier import classify_query
from app.services.retriever import retrieve_context
from app.services.resolver import resolve_ticket
from app.services.escalator import escalate_ticket

def classify_node(state: dict) -> dict:
    # FIX: Safely extract the query. 
    # Supports both string inputs and dictionary inputs with/without 'query' key.
    if isinstance(state, str):
        query_text = state
    elif isinstance(state, dict) and "query" in state:
        query_text = state["query"]
    else:
        # Fallback if input is malformed or empty
        query_text = ""

    # Run classification with the extracted text
    classification_result = classify_query(query_text)
    
    # Update state with classification results
    if isinstance(state, dict):
        state.update(classification_result)
        # Ensure the query is saved into the state for downstream nodes
        state["query"] = query_text
    else:
        # If state was just a string, we need to make it a dict now
        state = {"query": query_text}
        state.update(classification_result)
    
    return state

def retrieve_node(state: dict) -> dict:
    # FIX: Safely retrieve query using .get() to prevent crashes if missing
    query_text = state.get("query", "")
    state["context"] = retrieve_context(query_text)
    return state

def resolve_node(state: dict) -> dict:
    state["response"] = resolve_ticket(
        intent=state.get("intent", "general"),
        sub_intent=state.get("sub_intent"),
        query=state.get("query", ""),          # Safe fallback
        context=state.get("context", ""),
    )
    state["resolved"] = True
    state["needs_review"] = False
    return state

def escalate_node(state: dict) -> dict:
    state["response"] = escalate_ticket(state.get("query", "")) # Safe fallback
    state["resolved"] = False
    state["needs_review"] = True
    return state

def route_after_classification(state: dict) -> str:
    return "escalate" if state.get("confidence", 0) < 0.6 else "retrieve"

def route_after_retrieval(state: dict) -> str:
    return "resolve" if state.get("context") or state.get("confidence", 0) >= 0.6 else "escalate"