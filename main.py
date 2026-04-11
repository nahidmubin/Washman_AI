from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent
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

latest_query = ''

@app.post("/ask", response_class=HTMLResponse)
def ask(request: Request, query:Annotated[str, Form()]):
    global latest_query
    latest_query = query

    return templates.TemplateResponse(request, 'reply.html', {"query": latest_query})


@app.get("/stream", response_class=EventSourceResponse)
def reply():
    reply = washmans_reply(latest_query)
    for chunk in reply:
        yield ServerSentEvent(raw_data=chunk, event='message')
    yield ServerSentEvent(raw_data="done", event="close")