from fastapi import APIRouter, HTTPException
from app.schemas import TicketInput, ReviewInput
from app.graphs.ticket_graph import build_ticket_graph
from app.core.database import SessionLocal, engine
from app.models import TicketRecord
from app.core.database import Base

Base.metadata.create_all(bind=engine)

router = APIRouter()
graph = build_ticket_graph()

@router.post("/ticket")
def create_ticket(payload: TicketInput):
    result = graph.invoke({"query": payload.query})
    db = SessionLocal()
    ticket = TicketRecord(
        query=payload.query,
        intent=result.get("intent", "general"),
        sub_intent=result.get("sub_intent"),
        urgency=result.get("urgency", "low"),
        confidence=result.get("confidence", 0.0),
        context=result.get("context", ""),
        response=result.get("response", ""),
        resolved=result.get("resolved", False),
        needs_review=result.get("needs_review", False),
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.close()

    return {
        "id": ticket.id,
        "query": ticket.query,
        "intent": ticket.intent,
        "sub_intent": ticket.sub_intent,
        "urgency": ticket.urgency,
        "confidence": ticket.confidence,
        "entities": result.get("entities", []),
        "sentiment": result.get("sentiment", "neutral"),
        "context": ticket.context,
        "response": ticket.response,
        "resolved": ticket.resolved,
        "needs_review": ticket.needs_review,
    }

@router.get("/tickets")
def list_tickets():
    db = SessionLocal()
    tickets = db.query(TicketRecord).order_by(TicketRecord.id.desc()).all()
    db.close()
    return [
        {
            "id": t.id,
            "query": t.query,
            "intent": t.intent,
            "sub_intent": t.sub_intent,
            "urgency": t.urgency,
            "confidence": t.confidence,
            "response": t.response,
            "resolved": t.resolved,
            "needs_review": t.needs_review,
        }
        for t in tickets
    ]

@router.post("/tickets/{ticket_id}/review")
def review_ticket(ticket_id: int, payload: ReviewInput):
    db = SessionLocal()
    ticket = db.query(TicketRecord).filter(TicketRecord.id == ticket_id).first()
    if not ticket:
        db.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.resolved = payload.approved
    ticket.needs_review = False
    if payload.notes:
        ticket.response = f"{ticket.response}\n\nHuman notes: {payload.notes}"
    db.commit()
    db.refresh(ticket)
    db.close()

    return {"status": "updated", "ticket_id": ticket.id, "resolved": ticket.resolved}