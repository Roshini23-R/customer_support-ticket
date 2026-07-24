# AI Ticket Router & Resolver (FastAPI + LangGraph)

An AI-powered customer support ticket router and resolver built with FastAPI, LangGraph, and Retrieval-Augmented Generation (RAG). It classifies incoming support queries, searches a knowledge base, attempts automatic resolution, and escalates to a human reviewer when needed.

## Features

- AI-based **ticket classification** (e.g. billing, technical, account)
- Automatic **RAG-powered answers** using a vector store of FAQs/docs
- **Human-in-the-loop** review flow for complex or unresolved tickets
- REST API built with FastAPI, including interactive `/docs` UI
- LangGraph workflow for multi-step ticket processing
- Ready for deployment on Railway (free tier) with Docker support

## Tech Stack

- **Backend**: FastAPI (Python)
- **Agent framework**: LangGraph (+ LangChain components)
- **RAG / Vector store**: ChromaDB / langchain-chroma (or similar)
- **Embeddings**: sentence-transformers or langchain-huggingface
- **Server**: Uvicorn (ASGI)
- **Deployment**: GitHub + Railway (free cloud)

## Architecture Overview

1. Client sends a support query to the API.
2. LangGraph workflow:
   - Classify intent (billing / technical / general / etc.).
   - Retrieve relevant context from vector store (RAG).
   - Decide: resolve automatically or escalate to human.
3. FastAPI exposes:
   - `/ticket` – advanced LangGraph route via LangServe.
   - `/tickets` – simple REST endpoint for easy client usage.
4. Optional: human-review endpoints for tickets that were escalated.

## Project Structure

Example structure (adapted to your actual files):

```text
app/
  main.py              # FastAPI app entry
  models.py            # Pydantic models (TicketState, etc.)
  ticket_graph.py      # LangGraph workflow definition
  services/
    classifier.py      # Intent classification logic
    resolver.py        # Answer generation logic
    rag_store.py       # RAG ingest and retrieval
  rag/
    ingest.py          # Script to ingest docs/FAQs into vector store
    docs/              # Folder for .txt/.pdf docs (optional, for RAG)
```

Adjust names if your folder/file names differ.

## API Endpoints

Common endpoints (adapt this to your actual code):

- `POST /tickets`
  - Request: `{"query": "My billing is wrong"}`  
  - Response (example):
    ```json
    {
      "intent": "billing",
      "response": "Please check your last invoice in the billing portal...",
      "resolved": true,
      "needs_human_review": false
    }
    ```

- `POST /ticket/invoke` (LangGraph route via LangServe)
  - Advanced endpoint for streaming / graph-level interactions.

- `GET /docs`
  - FastAPI Swagger UI for testing all endpoints.

## Local Setup

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

python -m venv venv
source venv/bin/activate        # Linux/macOS
# or
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

If you don’t have `requirements.txt` yet, generate it from your venv:

```bash
pip freeze > requirements.txt
```

### 2. Prepare RAG docs (optional but recommended)

Create a `docs` folder under `app/rag/` and add `.txt` or `.pdf` files with FAQs or support documentation.

Example:

```text
app/rag/docs/
  faqs.txt
  billing_guide.pdf
```

Run the ingestion script:

```bash
python -m app.rag.ingest
```

This populates the vector store (e.g. ChromaDB) used for retrieval.

### 3. Run the API locally

```bash
uvicorn app.main:app --reload
```

Open:

- `http://localhost:8000/docs` to view and test endpoints.
- Try `POST /tickets` with sample queries.

## Deployment on Railway (Free Tier)

This project is designed to be deployed on Railway using GitHub integration.

### 1. Prepare Dockerfile (optional but recommended)

Add a `Dockerfile` in the project root:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Railway can either use this Dockerfile or run the app directly with a start command.

### 2. Push to GitHub

Initialize git and push (see instructions below in this README).

Once the repository is on GitHub (e.g. `https://github.com/<your-username>/ai-ticket-router`), you can connect it to Railway.

### 3. Create Railway project

1. Sign up or log in to [Railway](https://railway.com).
2. Click **New Project → Deploy from GitHub repo**.
3. Select your FastAPI repo.
4. Wait for Railway to build the app.

If Railway does not auto-detect the start command, set it manually in the service settings:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Railway sets `$PORT` automatically.

### 4. Environment variables (if needed)

If your app uses environment variables (e.g. `OPENAI_API_KEY`, `DB_URL`), define them in:

- Railway dashboard → your service → **Variables**.

For a basic version where everything is local/simple, you might not need any secrets.

### 5. Test the deployed API

Once deployment succeeds:

- Visit `https://<your-service>.up.railway.app/docs` to open FastAPI docs.
- Test `POST /tickets` with live queries.

You can share this URL on your resume and LinkedIn as live proof.

## Example Usage

```bash
curl -X POST "https://<your-service>.up.railway.app/tickets" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"My login is not working\"}"
```

Expected JSON output with intent, AI response, and resolution status.

## Future Improvements

Planned extensions:

- Full React / Bootstrap dashboard for ticket list and human review.
- Email or Slack integration to ingest real support tickets.
- More advanced RAG over multiple documents and knowledge bases.
- Analytics (ticket volume, resolution rate, escalation stats).

Even with the current backend MVP, this project demonstrates:

- AI agent workflow design with LangGraph.
- FastAPI production-style API.
- RAG integration for smarter answers.
- Human-in-the-loop design pattern.
