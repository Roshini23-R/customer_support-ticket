from pydantic import BaseModel
from typing import Optional, List

class TicketInput(BaseModel):
    query: str

class TicketResponse(BaseModel):
    id: int | None = None
    query: str
    intent: str
    sub_intent: Optional[str] = None
    urgency: str
    confidence: float
    entities: List[str] = []
    sentiment: str
    context: str
    response: str
    resolved: bool
    needs_review: bool = False

class ReviewInput(BaseModel):
    approved: bool
    notes: Optional[str] = None