from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langserve import add_routes
from .models import TicketRecord
from .graphs.ticket_graph import graph

app = FastAPI(title="Ticket Router API")

# LangGraph API routes (already existing)
add_routes(app, graph, path="/ticket")

@app.post("/tickets")
async def submit_ticket(query: str):
    result = await graph.ainvoke({"query": query})
    return result

# --- Frontend setup (new) ---
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Dummy data source; replace with your real DB or storage
from typing import List
from .models import TicketRecord  # adapt: include id, intent, response, resolved, needs_human_review

# For now, keep an in-memory list (you can replace later with DB)
TICKETS: List[TicketRecord] = []


@app.get("/dashboard")
async def dashboard(request: Request):
    # In real use, fetch tickets from DB / storage
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tickets": TICKETS},
    )


@app.get("/tickets/{ticket_id}")
async def ticket_detail(request: Request, ticket_id: int):
    # Simple lookup by id; adapt to your model
    ticket = next((t for t in TICKETS if t.id == ticket_id), None)
    if not ticket:
        # You can render an error page instead
        return templates.TemplateResponse(
            "ticket_detail.html",
            {"request": request, "ticket": None},
        )
    return templates.TemplateResponse(
        "ticket_detail.html",
        {"request": request, "ticket": ticket},
    )


@app.post("/tickets/{ticket_id}/review")
async def review_ticket(ticket_id: int, approved: bool):
    # Update ticket human review status
    for t in TICKETS:
        if t.id == ticket_id:
            t.needs_human_review = not approved
            # You might add fields like t.human_approved = approved
            break
    return {"ok": True, "ticket_id": ticket_id, "approved": approved}