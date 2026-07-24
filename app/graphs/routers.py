from fastapi import APIRouter
from app.models import TicketRequest
from app.graphs.ticket_graph import build_ticket_graph

router = APIRouter()
graph = build_ticket_graph()

@router.post("/ticket")
def create_ticket(payload: TicketRequest):
    result = graph.invoke({"query": payload.query})
    return {
        "query": payload.query,
        "intent": result.get("intent", "general"),
        "sub_intent": result.get("sub_intent"),
        "urgency": result.get("urgency", "low"),
        "confidence": result.get("confidence", 0.0),
        "entities": result.get("entities", []),
        "sentiment": result.get("sentiment", "neutral"),
        "context": result.get("context", ""),
        "response": result.get("response", ""),
        "resolved": result.get("resolved", False),
    }