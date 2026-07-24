from sqlalchemy import Column, Integer, String, Boolean, Float
from app.core.database import Base

class TicketRecord(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    intent = Column(String, default="general")
    sub_intent = Column(String, nullable=True)
    urgency = Column(String, default="low")
    confidence = Column(Float, default=0.0)
    context = Column(String, default="")
    response = Column(String, default="")
    resolved = Column(Boolean, default=False)
    needs_review = Column(Boolean, default=False)