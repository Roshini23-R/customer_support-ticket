from typing import List

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langserve import add_routes

from .models import TicketRecord
from .graphs.ticket_graph import graph

app = FastAPI(title="Ticket Router API")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


add_routes(app, graph, path="/ticket")


@app.post("/submit-form-ticket")
async def submit_ticket_form(query: str = Form(...)):
    result = await graph.ainvoke({"query": query})
    return result


TICKETS: List[TicketRecord] = []


@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "tickets": TICKETS},
    )


@app.get("/tickets/{ticket_id}")
async def ticket_detail(request: Request, ticket_id: int):
    ticket = next((t for t in TICKETS if t.id == ticket_id), None)
    return templates.TemplateResponse(
        "ticket_detail.html",
        {"request": request, "ticket": ticket},
    )


@app.post("/tickets/{ticket_id}/review")
async def review_ticket(ticket_id: int, approved: bool = Form(...)):
    for t in TICKETS:
        if t.id == ticket_id:
            t.needs_review = not approved
            break
    return {"ok": True, "ticket_id": ticket_id, "approved": approved}