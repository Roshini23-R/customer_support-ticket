# app/graphs/ticket_input.py
from pydantic import BaseModel

class TicketInput(BaseModel):
    query: str