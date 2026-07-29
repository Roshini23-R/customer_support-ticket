from app.services.classifier import classify_query
from app.services.retriever import retrieve_context
from app.services.resolver import resolve_ticket
from app.services.escalator import escalate_ticket


def classify_node(state: dict) -> dict:
    # state initially has {"query": ...}
    updates = classify_query(state["query"])
    # expected keys from classify_query: intent, sub_intent, urgency, confidence, maybe more
    state.update(updates)

    # initialize resolved / needs_review flags if not set
    state.setdefault("resolved", False)
    state.setdefault("needs_review", False)

    return state


def retrieve_node(state: dict) -> dict:
    # Retrieve context for the given query (you can make this real later)
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
    # If classification is low confidence, escalate; otherwise retrieve.
    return "escalate" if state.get("confidence", 0.0) < 0.6 else "retrieve"


def route_after_retrieval(state: dict) -> str:
    # If we have context or good confidence, resolve; otherwise escalate.
    if state.get("context") or state.get("confidence", 0.0) >= 0.6:
        return "resolve"
    return "escalate"