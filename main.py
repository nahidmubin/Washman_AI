from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from washman import washmans_reply


description = """
Washman AI is a demo AI assistant for Walton Washing Machines.
It uses Retrieval-Augmented Generation (RAG) and LLMs to answer user queries,
troubleshoot issues, and provide usage advice through a web interface.
"""

app = FastAPI(
    title="Washman AI",
    description=description,
    summary="Washman AI is a demo AI assistant for Walton Washing Machines",
    version="0.1",
    contact={
        "name": "Nahid Mubin",
        "url": "https://github.com/nahidmubin",
        "email": "nahidmubin@yahoo.com"
    }
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/", response_class=HTMLResponse)
def reply(request: Request, query:Annotated[str, Form()]):
    reply = washmans_reply(query)

    return templates.TemplateResponse(request, 'reply.html', {"query": query, "reply": reply})
