from app.services.classifier import classify_query
from app.services.retriever import retrieve_context
from app.services.resolver import resolve_ticket
from app.services.escalator import escalate_ticket

def classify_node(state: dict) -> dict:
    state.update(classify_query(state["query"]))
    return state

def retrieve_node(state: dict) -> dict:
    state["context"] = retrieve_context(state["query"])
    return state

def resolve_node(state: dict) -> dict:
    state["response"] = resolve_ticket(
        intent=state.get("intent", "general"),
        sub_intent=state.get("sub_intent"),
        query=state["query"],
        context=state.get("context", ""),
    )
    state["resolved"] = True
    state["needs_review"] = False
    return state

def escalate_node(state: dict) -> dict:
    state["response"] = escalate_ticket(state["query"])
    state["resolved"] = False
    state["needs_review"] = True
    return state

def route_after_classification(state: dict) -> str:
    return "escalate" if state.get("confidence", 0) < 0.6 else "retrieve"

def route_after_retrieval(state: dict) -> str:
    return "resolve" if state.get("context") or state.get("confidence", 0) >= 0.6 else "escalate"