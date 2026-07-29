# app/graphs/ticket_input.py
from typing import List, Optional, TypedDict

from pydantic import BaseModel


class TicketInput(BaseModel):
    """Slim schema LangServe uses to render the playground input box."""
    query: str


class TicketState(TypedDict, total=False):
    """Full graph state. TypedDict (unlike a narrow BaseModel) doesn't
    strip unknown keys on merge, so fields added by nodes (intent,
    context, response, etc.) survive through to the final output."""
    query: str
    intent: str
    sub_intent: Optional[str]
    confidence: float
    urgency: str
    entities: List[str]
    sentiment: str
    context: str
    response: str
    resolved: bool
    needs_review: bool